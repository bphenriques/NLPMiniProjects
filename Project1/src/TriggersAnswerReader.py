# -*- coding: utf-8 -*-

import re, Normalizer
from RegexUtil import RegexUtil

class TriggersAnswerReader:
    """
        Responsible for handling trigger and answers files and making queries over the data acquired.
    """
    __TRIGGER_TAG = "T"
    __ANSWER_TAG = "A"
    __trigger_regex = ""
    __answer_regex = ""
    __trigger_answers_dic = {}

    file_name = None

    def __init__(self, file_name):
        """
        Init

        :param file_name: File name of the file to be processed
        :return: instance of TriggersAnswerReader
        """
        self.file_name = file_name

        rew = RegexUtil()
        self.trigger_tag = rew.multiple_white_space() + self.__TRIGGER_TAG + rew.multiple_white_space() + "-" + rew.multiple_white_space()
        self.answer_tag = rew.multiple_white_space() + self.__ANSWER_TAG + rew.multiple_white_space() + "-" + rew.multiple_white_space()
        self.__trigger_regex = self.trigger_tag + rew.at_least_one(rew.anything)
        self.__answer_regex = self.answer_tag + rew.at_least_one(rew.anything)

    def process_file(self):
        """
        Processes file given in the constructor. If the execution completes, the data is stored and accessible
        using other methods (e.g. get_answer and get_answers). The triggers and answersmust happen on pairs
        in the following way:

        T - [Question]
        A - [Answer]

        """
        file_in = open(self.file_name, 'rU')

        while True:
            possible_trigger = file_in.readline()
            if not possible_trigger: break
            possible_answer = file_in.readline()
            if not possible_answer: break

            # Look for "T - Something?"
            trigger = self._read_trigger(possible_trigger)
            if len(trigger) == 0:
                continue

            # Look for "A - Something..."
            answer = self._read_answer(possible_answer)
            if len(answer) == 0:
                continue

            #processing triggers and answers as strings
            self._process_trigger_answer(''.join(trigger), ''.join(answer))

        file_in.close()

    def dump_map(self):
        """
        Prints the stored data about the triggers and the answers
        """
        print("Result: ", self.__trigger_answers_dic)

    # Update internal map of triggers and answers
    def _process_trigger_answer(self, trigger, answer):
        self._put(self.__trigger_normalizer(trigger), answer)

    # Adds element to the map, if the key already exists, append the value to the existing ones and updates the count
    # The list is always sorted by the most frequent to the least frequent
    def _put(self, trigger, response):
        if trigger not in self.__trigger_answers_dic:
            self.__trigger_answers_dic[trigger] = []

        list_tuples = self.__trigger_answers_dic[trigger]

        tuple_found = self._find_answer(list_tuples, response)
        if tuple_found is not None:
            new_tuple = (tuple_found[0], tuple_found[1] + 1)
            list_tuples.remove(tuple_found)
            list_tuples.append(new_tuple)
        else:
            new_tuple = (response, 1)
            list_tuples.append(new_tuple)

        #sort
        list_tuples.sort(key=lambda tup: tup[1], reverse=True)

    # trigger normalizer: lowercase, no punctuation and substituted the diacritics with the ascii equivalent character
    def __trigger_normalizer(self, trigger):
        return Normalizer.normalize_string(trigger)

    # reads the trigger using regex
    def _read_trigger(self, possible_trigger):
        return re.findall(self.__trigger_regex, possible_trigger)

    # reads the answer using regex
    def _read_answer(self, possible_answer):
        return re.findall(self.__answer_regex, possible_answer)

    def number_triggers(self):
        """
        :return: Number of existing triggers
        """
        return len(self.__trigger_answers_dic)

    '''Returns all answers given a trigger'''
    def get_answers(self, trigger):
        """
        Given a trigger, returns all possible answers sorted by the most frequent to the least frequent

        :param trigger: The question
        :return: sorted list of tuples (string, int), the first value is the answer and the second the #occurences
        """

        if trigger not in self.__trigger_answers_dic:
            return None

        return self.__trigger_answers_dic[trigger]

    def get_answer(self, trigger):
        """
        Given a trigger, returns the most probable answer. If there is draw, it is returned one of them
        :param trigger: The question
        :return: The answer (string)
        """

        if trigger not in self.__trigger_answers_dic:
            return None

        #first element of the returning tuple
        return self.get_answers(trigger)[0][0]



    #util: find tuple with a given name
    def _find_answer(self, tuplist, name):
        for tup in tuplist:
            if tup[0] == name:
                return tup
        return None