# -*- coding: utf-8 -*-

import re
from RegexUtil import RegexUtil

class TriggersAnswerReader:
    __TRIGGER_TAG = "T"
    __ANSWER_TAG = "A"
    __trigger_regex = ""
    __answer_regex = ""
    __questions_answers_map = {}

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
        print("Result: ", self.__questions_answers_map)


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
        #if __debug__:
        #    print "Adding ", response, " into ", " trigger ", trigger

        if trigger not in self.__questions_answers_map:
            self.__questions_answers_map[trigger] = []

        self.__questions_answers_map[trigger] += [response]

    def __trigger_normalizer(self, trigger):
        return trigger

    def _read_trigger(self, possible_trigger):
        return re.findall(self.__trigger_regex, possible_trigger)

    def _read_answer(self, possible_answer):
        return re.findall(self.__answer_regex, possible_answer)

    '''Number of triggers'''
    def number_triggers(self):
        return len(self.__questions_answers_map)

    '''Returns all answers given a question'''
    def get_answers(self, question):
        return self.__questions_answers_map[question]

    '''Returns the most probable trigger'''
    def get_answer(self, trigger):
        return "Gosto de bananas"

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

    def test_put(self):
        self.put("Question1", "Response1")
        assert(len(self.get_answers("Question1")) == 1)

        self.put("Question2", "Response1")
        self.put("Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)

        print("Passed Map of questions and responses")

    def test_process_file(self):
        self.process_file()
        assert self.number_triggers() > 0
        print "Passed reading file. Detected some triggers, the other tests covered the rest"



if __name__ == '__main__':
    questions_answer_reader = TestTriggersAnswerReader("src/TestResources/PerguntasPosSistema.txt")

    print "--- STARTING TESTS ---"
    questions_answer_reader.test_trigger_regex()
    questions_answer_reader.test_answer_regex()
    questions_answer_reader.test_process_file()
    print "--- END OF TESTS ---"
