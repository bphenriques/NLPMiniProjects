# -*- coding: utf-8 -*-

import re
from RegexUtil import RegexUtil

class TriggersAnswerReader:
    __TRIGGER_TAG = "T"
    __ANSWER_TAG = "A"
    __trigger_regex = ""
    __answer_regex = ""
    __trigger_answers_dic = {}

    file_name = None

    ''' Init, receives file_name '''
    def __init__(self, file_name):
        self.file_name = file_name

        rew = RegexUtil()
        self.trigger_tag = rew.multiple_white_space() + self.__TRIGGER_TAG + rew.multiple_white_space() + "-" + rew.multiple_white_space()
        self.answer_tag = rew.multiple_white_space() + self.__ANSWER_TAG + rew.multiple_white_space() + "-" + rew.multiple_white_space()
        self.__trigger_regex = self.trigger_tag + rew.at_least_one(rew.anything)
        self.__answer_regex = self.answer_tag + rew.at_least_one(rew.anything)

    ''' Reads file given by input and stores the associated triggers and the set of answers '''
    def process_file(self):
        fileIn = open(self.file_name, 'rU')
        self._get_triggers_and_answers(fileIn)
        fileIn.close()

    ''' Print internal representation of map of triggers and answers'''
    def dump_map(self):
        print("Result: ", self.__trigger_answers_dic)


    ''' Reads the file 2 lines at a time and processes the corresponding trigger and answer if exists using regex '''
    def _get_triggers_and_answers(self, file_in):
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

    ''' Update internal map of triggers and answers'''
    def _process_trigger_answer(self, trigger, answer):
        #Update internal map of triggers and answers
        self._put(self.__trigger_normalizer(trigger), answer)

    '''Adds element to the map, if the key already exists, append the value to the existing ones'''
    def _put(self, trigger, response):
        if trigger not in self.__trigger_answers_dic:
            self.__trigger_answers_dic[trigger] = []

        list_tuples = self.__trigger_answers_dic[trigger]

        tuple_found = self._find_answer(list_tuples, response)
        if tuple_found is not None:
            new_tuple = self._increment_count(tuple_found)
            list_tuples.remove(tuple_found)
            list_tuples.append(new_tuple)
        else:
            new_tuple = (response, 1)
            list_tuples.append(new_tuple)


    def __trigger_normalizer(self, trigger):
        return trigger

    def _read_trigger(self, possible_trigger):
        return re.findall(self.__trigger_regex, possible_trigger)

    def _read_answer(self, possible_answer):
        return re.findall(self.__answer_regex, possible_answer)

    '''Number of triggers'''
    def number_triggers(self):
        return len(self.__trigger_answers_dic)

    '''Returns all answers given a trigger'''
    def get_answers(self, trigger):
        if trigger not in self.__trigger_answers_dic:
            return None

        return self.__trigger_answers_dic[trigger]

    '''Returns the most probable trigger'''
    def get_answer(self, trigger):
        if trigger not in self.__trigger_answers_dic:
            return None

        list_responses = self.__trigger_answers_dic[trigger]


        return "Gosto de bananas"

    def _find_answer(self, tuplist, name):
        for tup in tuplist:
            if tup[0] == name:
                return tup
        return None

    '''Returns a new tuple with the same response but with incremented count'''
    def _increment_count(self, tuple):
        name = tuple[0]
        count = tuple[1]
        return (name, count+1)

#For testing
class TestTriggersAnswerReader(TriggersAnswerReader):
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

    def test_answer_regex(self):
        count = 0
        for answer in self.__test_answers:
            result = self._read_answer(answer)
            if len(result) > 0:
                count += 1

        assert(len(self.__test_answers) == count)
        print "Passed ", count, " tests reading answers"

    def test_trigger_regex(self):
        count = 0
        for trigger in self.__test_triggers:
            result = self._read_trigger(trigger)
            if len(result) > 0:
                count += 1

        assert(len(self.__test_triggers) == count)
        print "Passed ", count, " tests reading triggers"

    def test_data_structure(self):
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

    def test_find_response_in_list_tuples(self):
        list_tuples = [("Banana", 1), ("Morango", 3), ("Ananas", 5)]
        found_tuple = self._find_answer(list_tuples, "Ananas")
        list_tuples.remove(found_tuple)
        new_tuple = (found_tuple[0], found_tuple[1]+1)
        list_tuples.append(new_tuple)
        print "New tuple ", new_tuple
        print "New list ", list_tuples



    def test_process_file(self):
        self.process_file()
        assert self.number_triggers() > 0
        print "Passed reading file. Detected some triggers, the other tests covered the rest"



if __name__ == '__main__':
    questions_answer_reader = TestTriggersAnswerReader("src/TestResources/PerguntasPosSistema.txt")

    print "--- STARTING TESTS ---"
    #questions_answer_reader.test_trigger_regex()
    #questions_answer_reader.test_answer_regex()
    #questions_answer_reader.test_find_response_in_list_tuples()
    questions_answer_reader.test_data_structure()
    #questions_answer_reader.test_process_file()
    print "--- END OF TESTS ---"
