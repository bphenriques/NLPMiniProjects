# -*- coding: utf-8 -*-

import re
import os.path
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

    __user_input_tag_regex = r"^[\s]*" + "User Input:" + r"[\s]*"
    __trigger_tag_regex = r"^[\s]*" + "T" + r"[\s]*" + "-" + r"[\s]*"
    __answer_tag_regex = r"^[\s]*" + "A" + r"[\s]*" + "-" + r"[\s]*"

    __user_input_regex = None
    __trigger_regex = None
    __answer_regex = None

    __user_input_answers_dic = {}

    _file_name = None

    def __init__(self):
        # pre-computing regex expressions
        self.__user_input_regex = self.__user_input_tag_regex + ".*$"
        self.__trigger_regex = self.__trigger_tag_regex + ".*$"
        self.__answer_regex = self.__answer_tag_regex + ".*$"

    def process_file(self, file_name):
        """
        Processes file given by argument. If the execution completes, the data is stored and accessible
        using other methods (e.g. get_answer and get_answers).

        If searches for "User Input: " followed by pairs of triggers ("T - ...") or answers ("A - ...")

        If the file does not exist, an exception is thrown

        :param: _file_name, the path to the file
        """

        if not os.path.exists(file_name):
            print "File not found"
            raise Exception

        self._file_name = file_name

        file_in = open(self._file_name, 'rU')
        while True:
            possible_user_input = file_in.readline()
            if not possible_user_input: break  # EOF

            # Read "User Input: Something"
            user_input = self._read_user_input(possible_user_input)
            if user_input is None: continue  # keep looking for

            # loop until next "User Input: Something" is found
            potential_next_user_input = None
            while potential_next_user_input is None:
                input = file_in.readline()
                if not input: break  # EOF

                # print "potential_next_user_input: ", input
                potential_next_user_input = self._read_user_input(input)

                # haven't reached the next user input
                if potential_next_user_input is None:

                    # Is it "T - Something?"
                    trigger = self._read_trigger(input)
                    if trigger is None: continue

                    # if so, next line must be "A - Something"
                    possible_answer = file_in.readline()
                    if not possible_answer: break  # EOF

                    # Look for "A - Something..."
                    answer = self._read_answer(possible_answer)
                    if answer is None: continue

                    self._process_user_input_answer(user_input, trigger, answer)
                else:
                    user_input = potential_next_user_input
                    potential_next_user_input = None
                    continue

        file_in.close()

    def dump_map(self):
        """
        Prints the stored data regarding user input and the possible answers
        """
        for key, answers in self.__user_input_answers_dic.iteritems():
            print "User_Input:", key
            for answer in answers:
                print "\t[", answer[1], "]", answer[0]

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
        self._file_name = None
        self.__user_input_answers_dic = {}

    # Update internal map of triggers and answers
    def _process_user_input_answer(self, user_input, trigger, answer):
        # print "user_input: ", user_input
        # print "\ttrigger: ", trigger
        # print "\t\tanswer: ", answer

        if isinstance(user_input, str): user_input = user_input.decode("utf-8")
        if isinstance(trigger, str): trigger = trigger.decode("utf-8")
        if isinstance(answer, str): answer = answer.decode("utf-8")

        if user_input not in self.__user_input_answers_dic:
            self.__user_input_answers_dic[user_input] = []

        #check if userinput exists literraly, if so:
        #   if I found out already a identical answer, append the element to the list
        #   else, I delete athe element and set a flag as true

        #else, if there is no answer with identical trigger, keep adding similar
        #   else, ignore if it is not similar

        if self._is_similar_enough(user_input, trigger):
            self._put(user_input, self._normalize_answer(answer))

    #verify using word/sentence distance if a trigger is close enough
    def _is_similar_enough(self, user_input, trigger):
        return self._normalize_user_input(user_input) == self._normalize_trigger(trigger)

    # Adds element to the map, if the key already exists, append the value to the existing ones and updates the count
    # The list is always sorted by the most frequent to the least frequent
    def _put(self, user_input, answer):
        list_tuples = self.__user_input_answers_dic[user_input]

        tuple_found = self._find_answer(list_tuples, answer)
        if tuple_found is not None:
            new_tuple = (tuple_found[0], tuple_found[1] + 1)
            list_tuples.remove(tuple_found)
            list_tuples.append(new_tuple)
        else:
            new_tuple = (answer, 1)
            list_tuples.append(new_tuple)

        # sort
        list_tuples.sort(key=lambda tup: tup[1], reverse=True)

    def _normalize_user_input(self, user_input):
        # lowercase, no punctuation diacritics transformation
        return RegexUtil.normalize_string(user_input)

    def _normalize_trigger(self, trigger):
        # lowercase, no punctuation diacritics transformation
        return RegexUtil.normalize_string(trigger)

    def _normalize_answer(self, answer):
        return answer

    # reads the trigger using regex
    def _read_trigger(self, possible_trigger):
        found_regex = re.search(self.__trigger_regex, possible_trigger)
        if found_regex is None: return None

        return re.sub(self.__trigger_tag_regex, '', found_regex.string).strip()

    # reads the answer using regex
    def _read_answer(self, possible_answer):
        found_regex = re.search(self.__answer_regex, possible_answer)
        if found_regex is None: return None

        return re.sub(self.__answer_tag_regex, '', found_regex.string).strip()

    # Reads user input using regex
    def _read_user_input(self, possible_input):
        found_regex = re.search(self.__user_input_regex, possible_input)
        if found_regex is None: return None

        return re.sub(self.__user_input_tag_regex, '', found_regex.string).strip()

    # util: find tuple with a given name
    def _find_answer(self, tup_list, name):
        for tup in tup_list:
            if tup[0] == name:
                return tup
        return None
