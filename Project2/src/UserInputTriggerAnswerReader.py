# -*- coding: utf-8 -*-

import re
import os.path


class UserInputTriggerAnswerReader:
    __user_input_tag_regex = r"^[\s]*" + "User Input:" + r"[\s]*"
    __trigger_tag_regex = r"^[\s]*" + "T" + r"[\s]*" + "-" + r"[\s]*"
    __answer_tag_regex = r"^[\s]*" + "A" + r"[\s]*" + "-" + r"[\s]*"

    __user_input_regex = None
    __trigger_regex = None
    __answer_regex = None

    def __init__(self):
        self.__user_input_regex = self.__user_input_tag_regex + ".*$"
        self.__trigger_regex = self.__trigger_tag_regex + ".*$"
        self.__answer_regex = self.__answer_tag_regex + ".*$"

    def process_file(self, file_name, process_user_input_answer_callback):

        """
        Processes file given by argument. If the execution completes, the data is stored and accessible
        using other methods (e.g. get_answer and get_answers).

        If searches for "User Input: " followed by pairs of triggers ("T - ...") or answers ("A - ...")

        If the file does not exist, an exception is thrown

        :param: _file_name, the path to the file
        :param: process_user_input_answer_callback, call back function that receives, user_input, trigger and answer
        """

        if not os.path.exists(file_name):
            print "File not found"
            raise Exception

        file_in = open(file_name, 'rU')
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

                    process_user_input_answer_callback(user_input, trigger, answer)
                else:
                    user_input = potential_next_user_input
                    potential_next_user_input = None
                    continue

        file_in.close()

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