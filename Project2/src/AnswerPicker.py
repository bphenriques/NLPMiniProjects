# -*- coding: utf-8 -*-

import StrategiesForTriggers as st
import StrategiesForAnswers as sa
from RegexUtil import RegexUtil


class AnswerPickerAnswerResult:
    def __init__(self):
        pass

    INVALID_USER_INPUT = 0
    TRIGGER_NOT_FOUND = 1


class AnswerPicker:
    """
        Responsible for handling user_input, the corpus file and all possible answers.
    """

    def __init__(self, file_reader, trigger_strategy=st.IdenticalNormalized(), answer_strategy=sa.Identical()):
        self.__user_input_answers_dic = {}
        self.__user_input_identical_trigger_found_flags = {}
        self._file_reader = file_reader
        self._trigger_strategy = trigger_strategy
        self._answer_strategy = answer_strategy

    def dump_map(self):
        """
        Prints the stored data regarding user input and the possible answers
        """
        for key, answers in self.__user_input_answers_dic.iteritems():
            print "User_Input:", key
            for answer in answers:
                print "\t[", answer[1], "]", answer[0]

    def _dump_flags(self):
        for key, flag in self.__user_input_identical_trigger_found_flags.iteritems():
            print flag, "-->", key

    def number_matched_user_input(self):
        """
        :return: Number of existing triggers
        """
        return len(self.__user_input_answers_dic)

    def get_answers(self, user_input):
        """
        Given a user_input, returns all possible answers sorted by the most frequent to the least frequent

        :param user_input
        :return: sorted list of tuples (string, int), the first value is the answer and the second the #occurences
                 if there is no answers, a empty list is returned
        """

        if isinstance(user_input, str): user_input = user_input.decode("utf-8")
        user_input = RegexUtil.custom_strip(user_input)
        if user_input not in self.__user_input_answers_dic:
            return None

        return self.__user_input_answers_dic[user_input]

    def get_answer(self, user_input):
        """
        Given a user_input, returns the most probable answer. If there is draw, it is returned one of them

        :param user_input
        :return: The answer (string)
        """

        if isinstance(user_input, str): user_input = user_input.decode("utf-8")
        user_input = RegexUtil.custom_strip(user_input)
        answers = self.get_answers(user_input)
        if answers is None:
            return AnswerPickerAnswerResult.INVALID_USER_INPUT
        if len(answers) == 0:
            return AnswerPickerAnswerResult.TRIGGER_NOT_FOUND
        else:
            return answers[0][0]  # [first answer] [first element tuple]

    def clear(self):
        """
        Clears the internal map of user_inputs and answers
        """
        self.__user_input_answers_dic = {}
        self.__user_input_identical_trigger_found_flags = {}

    def process_user_input_answer(self, user_input, trigger, answer):
        """

        :param user_input:
        :param trigger:
        :param answer:
        :return:
        """

        if isinstance(user_input, str): user_input = user_input.decode("utf-8")
        if isinstance(trigger, str): trigger = trigger.decode("utf-8")
        if isinstance(answer, str): answer = answer.decode("utf-8")

        if user_input not in self.__user_input_answers_dic:
            self.__user_input_answers_dic[user_input] = []

        # if user input is literally identical
        if self._trigger_strategy.is_user_input_trigger_identical(user_input, trigger):

            # if it is filled with similar stuff, delete because we already have a full match
            if user_input not in self.__user_input_identical_trigger_found_flags:
                self.__user_input_answers_dic[user_input] = []

            self._put(user_input, answer)
            self.__user_input_identical_trigger_found_flags[user_input] = True

        elif user_input not in self.__user_input_identical_trigger_found_flags and \
                self._trigger_strategy.is_user_input_trigger_similar(user_input, trigger):
            self._put(user_input, answer)



    # Adds element to the map, if the key already exists, append the value to the existing ones and updates the count
    # The list is always sorted by the most frequent to the least frequent
    def _put(self, user_input, answer):
        list_tuples = self.__user_input_answers_dic[user_input]

        new_tuple = (answer, 1)
        tuple_found = self._find_answer(list_tuples, answer)
        if tuple_found is not None:
            new_tuple = (tuple_found[0], tuple_found[1] + 1)
            list_tuples.remove(tuple_found)

        list_tuples.append(new_tuple)
        list_tuples.sort(key=lambda tup: tup[1], reverse=True) #  sort

    # util: find tuple with a given name
    def _find_answer(self, tup_list, name):
        for tup in tup_list:
            if self._answer_strategy.are_answer_similar_enough(tup[0], name):
                return tup
        return None
