# -*- coding: utf-8 -*-

import re
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
        return trigger

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

#For testing
class TestTriggersAnswerReader(TriggersAnswerReader):
    """
    Test class for TriggersAnswersReader
    """
    __test_triggers = [
        " T - És mesmo parolo!",
        " T - Eu vou à loja do mestra André. É mesmo aqui ao lado!",
        " T - ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ. Derp. Não estou a dizer coisa com coisa (estou?)...",
        " T - E então ele disse: \"Cenas engraçadas",
        " T - E então ele disse: \"Dás me o teu número?",
        " T - Estou preguiçoso. Vou escrever mal. Queres ìr alìh? È que...è que ? Sìgh!"
    ]

    __test_answers = [
        " A - És mesmo parolo!",
        " A - Eu vou à loja do mestra André. É mesmo aqui ao lado!",
        " A - ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ. Derp. Não estou a dizer coisa com coisa (estou?)...",
        " A - E então ele disse: \"Cenas engraçadas",
        " A - E então ele disse: \"Dás me o teu número?",
        " A - Estou preguiçoso. Vou escrever mal. Queres ìr alìh? È que...è que ? Sìgh!"
    ]

    def test_answer_regex(self, lst=None):
        """
        Tests if all sentences in the list given by argument are ALL answers. True positives only.
        If any violates, an assertion will fail.

        :param lst: optional argument. List of strings
        """

        if lst is None:
            lst = self.__test_answers

        count = 0
        for answer in lst:
            result = self._read_answer(answer)
            if len(result) > 0:
                count += 1

        assert(len(self.__test_answers) == count)
        print "Passed ", count, " tests reading answers"

    def test_trigger_regex(self, lst=None):
        """
        Tests if all sentences in the list given by argument are ALL triggers. True positives only.

        :param lst: optional argument. List of strings
        """
        if lst is None:
            lst = self.__test_triggers

        count = 0
        for trigger in lst:
            result = self._read_trigger(trigger)
            if len(result) > 0:
                count += 1

        assert(len(self.__test_triggers) == count)
        print "Passed ", count, " tests reading triggers"

    def test_data_structure(self):
        """
        Tests the internal data structure. Checks if the stored answers are correct and if the queries returns the
        expected results.
        """
        #Test one addition
        self._put("Question1", "Response1")
        assert(len(self.get_answers("Question1")) == 1)

        #Test multiple responses for same question
        self._put("Question2", "Response1")
        self._put("Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)

        #Test same response for same question and therefore should increment
        self._put("Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)
        answers = self.get_answers("Question2")
        assert answers is not None
        answer = self._find_answer(answers, "Response2")
        assert answer is not None
        assert answer[0] == "Response2"
        assert answer[1] == 2

        #Find non-existent trigger
        non_existent_trigger = self.get_answers("Bla")
        assert non_existent_trigger is None
        non_existent_trigger = self.get_answer("Bla")
        assert non_existent_trigger is None

        print("Passed all tests regarding data structures")

    def test_sort(self):
        """
        Tests if the  answers stored are sorted from the most frequent to the least frequent
        """
        self._put("TestQuestion2", "Response1")
        self._put("TestQuestion2", "Response2")
        self._put("TestQuestion2", "Response3")
        self._put("TestQuestion2", "Response3") #Response3 : 2
        self._put("TestQuestion2", "Response3") #Response3 : 3
        self._put("TestQuestion2", "Response3") #Response3 : 4
        self._put("TestQuestion2", "Response2") #Response2 : 2
        self._put("TestQuestion2", "Response1") #Response1 : 2
        self._put("TestQuestion2", "Response2") #Response2 : 3
        self._put("TestQuestion2", "Response4") #Response4 : 1
        self._put("TestQuestion2", "Response5") #Response5 : 1

        answers = self.get_answers("TestQuestion2")
        assert answers[0][0] == "Response3"
        assert answers[1][0] == "Response2"
        assert answers[2][0] == "Response1"
        assert answers[3][0] == "Response5" or answers[3][0] == "Response4"
        assert answers[4][0] == "Response5" or answers[4][0] == "Response4"

        print "Passed sort test"

    def test_get_answer(self):
        """
        Tests if it is return the most frequent answer
        """
        self._put("TestQuestion1", "Response1")
        self._put("TestQuestion1", "Response2")
        self._put("TestQuestion1", "Response3")
        self._put("TestQuestion1", "Response3") #Response3 : 2
        self._put("TestQuestion1", "Response3") #Response3 : 3
        self._put("TestQuestion1", "Response3") #Response3 : 4
        self._put("TestQuestion1", "Response2") #Response2 : 2
        self._put("TestQuestion1", "Response1") #Response1 : 2
        self._put("TestQuestion1", "Response2") #Response2 : 3
        self._put("TestQuestion1", "Response4") #Response4 : 1
        self._put("TestQuestion1", "Response5") #Response5 : 1

        #Response3 is most frequent: 4
        assert self.get_answer("TestQuestion1") == "Response3"

        #changing the leadership
        self._put("TestQuestion1", "Response2") #Response2 : 4
        self._put("TestQuestion1", "Response2") #Response2 : 5

        #Response2 is most frequent: 5
        assert self.get_answer("TestQuestion1") == "Response2"

        #Response3 and Response2 are 5 (draw)
        self._put("TestQuestion1", "Response3") #Response3 : 5
        assert self.get_answer("TestQuestion1") == "Response2" or self.get_answer("TestQuestion1") == "Response3"

        print "Passed get response test"


    def test_process_file(self):
        """
        Tests if the file is processed correctly
        """
        self.process_file()
        assert self.number_triggers() > 0
        print "Passed reading file. Detected some triggers, the other tests covered the rest"



if __name__ == '__main__':
    questions_answer_reader = TestTriggersAnswerReader("TestResources/PerguntasPosSistema.txt")

    print "--- STARTING TESTS ---"
    questions_answer_reader.test_trigger_regex()
    questions_answer_reader.test_answer_regex()
    questions_answer_reader.test_data_structure()
    questions_answer_reader.test_sort()
    questions_answer_reader.test_get_answer()
    questions_answer_reader.test_process_file()
    print "--- END OF TESTS ---"
