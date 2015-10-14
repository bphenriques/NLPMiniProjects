# -*- coding: utf-8 -*-

import re
import os.path
from RegexUtil import RegexUtil

class TriggersAnswerReader:
    """
        Responsible for handling user_input and all possible answers.
    """
    __USER_INPUT_TAG = "User Input: "
    __TRIGGER_TAG = "T"
    __ANSWER_TAG = "A"
    __trigger_regex = ""
    __answer_regex = ""
    __user_input_answers_dic = {}

    __user_input_regex = None
    __trigger_tag_regex = None
    __answer_tag_regex = None

    file_name = None

    def __init__(self):

        # pre-computing regex expressions
        rew = RegexUtil()
        self.__trigger_tag_regex = rew.multiple_white_space() + self.__TRIGGER_TAG + rew.multiple_white_space() + "-" + rew.multiple_white_space()
        self.__answer_tag_regex = rew.multiple_white_space() + self.__ANSWER_TAG + rew.multiple_white_space() + "-" + rew.multiple_white_space()
        self.__trigger_regex = self.__trigger_tag_regex + rew.at_least_one(rew.anything)
        self.__answer_regex = self.__answer_tag_regex + rew.at_least_one(rew.anything)

        self.__user_input_regex = self.__USER_INPUT_TAG + rew.multiple_white_space() + rew.any(rew.anything)

    def process_file(self, file_name):
        """
        Processes file given by argument. If the execution completes, the data is stored and accessible
        using other methods (e.g. get_answer and get_answers).

        If searches for "User Input: " followed by pairs of triggers ("T - ...") or answers ("A - ...")

        If the file does not exist, an exception is thrown

        :param: file_name, the path to the file
        """

        if not os.path.exists(file_name):
            print "Either file is missing or is not readable"
            raise Exception

        self.file_name = file_name

        file_in = open(self.file_name, 'rU')
        while True:
            possible_user_input = file_in.readline()
            if not possible_user_input: break #EOF

            #Read "User Input: Something"
            user_input = self._read_user_input(possible_user_input)
            if user_input is None: continue #keep looking for

            #print "user_input: ", user_input

            #loop until next "User Input: Something" is found
            potential_next_user_input = None
            while potential_next_user_input is None:
                input = file_in.readline()
                if not input: break #EOF

                #print "potential_next_user_input: ", input
                potential_next_user_input = self._read_user_input(input)

                #haven't reached the next user input
                if potential_next_user_input is None:

                    # Is it "T - Something?"
                    trigger = self._read_trigger(input)
                    if trigger is None: continue

                    #if so, next line must be "A - Something"
                    possible_answer = file_in.readline()
                    if not possible_answer: break #EOF

                    # Look for "A - Something..."
                    answer = self._read_answer(possible_answer)
                    if answer is None: continue

                    #print "\ttrigger: ", trigger
                    #print "\t\tanswer: ", answer

                    normalized_user_input = self.normalize_user_input(user_input)
                    normalized_trigger = self.normalize_user_input(trigger)
                    if normalized_trigger == normalized_user_input:
                        self._process_user_input_answer(normalized_user_input, answer)
                else:
                    user_input = potential_next_user_input
                    potential_next_user_input = None
                    #print "user_input: ", user_input
                    continue

        file_in.close()

    def dump_map(self):
        """
        Prints the stored data regarding user input and the possible answers
        """
        for key, answers in self.__user_input_answers_dic.iteritems():
            print "User_Input: ", key
            for answer in answers:
                print "\t[", answer[1], "] ", answer[0].decode("utf-8")

    # Update internal map of triggers and answers
    def _process_user_input_answer(self, user_input, answer):
        self._put(self.normalize_user_input(user_input), self.normalize_answer(answer))

    # Adds element to the map, if the key already exists, append the value to the existing ones and updates the count
    # The list is always sorted by the most frequent to the least frequent
    def _put(self, trigger, answer):
        if trigger not in self.__user_input_answers_dic:
            self.__user_input_answers_dic[trigger] = []

        list_tuples = self.__user_input_answers_dic[trigger]

        tuple_found = self._find_answer(list_tuples, answer)
        if tuple_found is not None:
            new_tuple = (tuple_found[0], tuple_found[1] + 1)
            list_tuples.remove(tuple_found)
            list_tuples.append(new_tuple)
        else:
            new_tuple = (answer, 1)
            list_tuples.append(new_tuple)

        #sort
        list_tuples.sort(key=lambda tup: tup[1], reverse=True)

    # user_input normalizer: lowercase, no punctuation and substituted the diacritics with the ascii equivalent character
    def normalize_user_input(self, user_input):
        rxutil = RegexUtil()
        return rxutil.normalize_string(user_input)

    def normalize_answer(self, answer):
        return answer

    # reads the trigger using regex
    def _read_trigger(self, possible_trigger):
        found_regex = re.findall(self.__trigger_regex, possible_trigger)
        if len(found_regex) == 0: return None

        return re.sub(self.__trigger_tag_regex, '', ''.join(found_regex))

    # reads the answer using regex
    def _read_answer(self, possible_answer):
        found_regex = re.findall(self.__answer_regex, possible_answer)
        if len(found_regex) == 0: return None

        return re.sub(self.__answer_tag_regex, '', ''.join(found_regex))

    # Reads user input using regex
    def _read_user_input(self, possible_input):
        found_regex = re.findall(self.__user_input_regex, possible_input)
        if len(found_regex) == 0: return None

        return re.sub(self.__USER_INPUT_TAG, '', ''.join(found_regex))

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

        normalized_trigger = self.normalize_user_input(user_input)
        if normalized_trigger not in self.__user_input_answers_dic:
            return list()

        return self.__user_input_answers_dic[normalized_trigger]

    def get_answer(self, user_input):
        """
        Given a user_input, returns the most probable answer. If there is draw, it is returned one of them

        :param user_input
        :return: The answer (string)
        """

        normalized_trigger = self.normalize_user_input(user_input)
        if normalized_trigger not in self.__user_input_answers_dic:
            return None

        #first element of the returning tuple
        return self.get_answers(normalized_trigger)[0][0]



    #util: find tuple with a given name
    def _find_answer(self, tuplist, name):
        for tup in tuplist:
            if tup[0] == name:
                return tup
        return None

    def clear(self):
        self.file_name = None
        self.__user_input_answers_dic = {}