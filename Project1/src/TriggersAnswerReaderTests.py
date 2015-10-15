# -*- coding: utf-8 -*-

from TriggersAnswerReader import TriggersAnswerReader

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
        assert "Stuff cute" == self._read_answer("A - Stuff cute")

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
        assert("Stuff cute" == self._read_trigger("T - Stuff cute"))
        print "Passed ", count, " tests reading triggers"

    def test_data_structure(self):
        """
        Tests the internal data structure. Checks if the stored answers are correct and if the queries returns the
        expected results. Don't forget that the strings are normalized
        """
        #Test one addition
        self._process_user_input_answer("Question1", "Question1", "Response1")
        assert(len(self.get_answers("Question1")) == 1)

        #Test multiple responses for same question
        self._process_user_input_answer("Question2", "Question2", "Response1")
        self._process_user_input_answer("Question2", "Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)

        #Test same response for same question and therefore should increment
        self._process_user_input_answer("Question2", "Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)
        answers = self.get_answers("Question2")
        assert answers is not None
        answer = self._find_answer(answers, self.normalize_answer("Response2"))
        assert answer is not None
        assert answer[0] == self.normalize_answer("Response2")
        assert answer[1] == 2

        #Find non-existent trigger
        non_existent_trigger = self.get_answers("Bla")
        assert len(non_existent_trigger) == 0
        non_existent_trigger = self.get_answer("Bla")
        assert non_existent_trigger is None

        print("Passed all tests regarding data structures")

    def test_sort(self):
        """
        Tests if the  answers stored are sorted from the most frequent to the least frequent
        """
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response1")
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2")
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3") #Response3 : 2
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3") #Response3 : 3
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3") #Response3 : 4
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2") #Response2 : 2
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response1") #Response1 : 2
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2") #Response2 : 3
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response4") #Response4 : 1
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response5") #Response5 : 1

        answers = self.get_answers("TestQuestion2")
        assert answers[0][0] == self.normalize_answer("Response3")
        assert answers[1][0] == self.normalize_answer("Response2")
        assert answers[2][0] == self.normalize_answer("Response1")
        assert answers[3][0] == self.normalize_answer("Response5") or \
               answers[3][0] == self.normalize_answer("Response4")
        assert answers[4][0] == self.normalize_answer("Response5") or \
               answers[4][0] == self.normalize_answer("Response4")

        print "Passed sort test"

    def test_get_answer(self):
        """
        Tests if it is return the most frequent answer
        """

        self.clear()
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response1")
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3") #Response3 : 2
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3") #Response3 : 3
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3") #Response3 : 4
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2") #Response2 : 2
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response1") #Response1 : 2
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2") #Response2 : 3
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response4") #Response4 : 1
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response5") #Response5 : 1

        #Response3 is most frequent: 4
        assert self.get_answer("TestQuestion1") == self.normalize_answer("Response3")

        #changing the leadership
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2") #Response2 : 4
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2") #Response2 : 5

        #Response2 is most frequent: 5
        assert self.get_answer("TestQuestion1") == self.normalize_answer("Response2")

        #Response3 and Response2 are 5 (draw)
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3") #Response3 : 5
        assert self.get_answer("TestQuestion1") == self.normalize_answer("Response2") or \
               self.get_answer("TestQuestion1") == self.normalize_answer("Response3")

        print "Passed get response test"


    def test_normalizer(self):
        """
        Tests normalize string
        """

        self.clear()
        self._process_user_input_answer("TestQuestion3", "TestQuestion3", "Response1")
        self._process_user_input_answer("TestQuestion3", "TéstQuestion3", "Response2")
        self._process_user_input_answer("TestQuestion3", "TéstQuestion3.", "Response3")
        self._process_user_input_answer("TestQuestion3", "Tést,Quèstíõn3.", "Response4")
        self._process_user_input_answer("TestQuestion3", "Tèst,Questiôn3.", "Response5")
        self._process_user_input_answer("TestQuestion3", "Tést,Question3.", "Response6")
        self._process_user_input_answer("TestQuestion3", "Tést,QUESTION3.", "Response7")
        self._process_user_input_answer("TestQuestion3", "Tést,QUESTION3.\n", "Response8")
        self._process_user_input_answer("TestQuestion3", "Tést!,QUESTION3.\n", "Response9")
        self._process_user_input_answer("TestQuestion3", "Tést!,QU:ES;TI,ON?3.\n", "Response10")
        self._process_user_input_answer("TestQuestion3", "Tést!,QU:ES;TI,ON?3.\n", "Response11")
        self._process_user_input_answer("TestQuestion3", "Tést!,\"QU:ES;TI,O\"N?3.\r\n", "Response12")
        self._process_user_input_answer("TestQuestion3", "Té)s(t!,\"QU:E(S;TI,O\"N?3.\n", "Response13")
        self._process_user_input_answer("TestQuestion3", "Té)s(t!,\"QU:E(S;TÍ,Õ\"N?3.\n", "Response13")

        assert len(self.get_answers("TestQuestion3")) == 13

        print "Passed normalization test"

    def test_read_user_input(self):
        assert "Bla bla bla" == self._read_user_input("User Input: Bla bla bla")
        assert self._read_user_input("GIBBERISH") is None
        assert self._read_user_input("user input: asdhasdh") is None
        print "Success reading user input"


    def test_process_file(self, file_name):
        """
        Tests if the file is processed correctly
        """
        self.clear()
        self.process_file(file_name)
        assert self.number_matched_user_input() == 1
        assert len(self.get_answers("Tens filhos?")) == 12
        assert self.get_answer("Tens filhos?") == "Não."
        print "Passed reading file. Detected some triggers, the other tests covered the rest"


if __name__ == '__main__':
    questions_answer_reader = TestTriggersAnswerReader()

    print "--- STARTING TESTS ---"
    questions_answer_reader.test_read_user_input()
    questions_answer_reader.test_trigger_regex()
    questions_answer_reader.test_answer_regex()
    questions_answer_reader.test_normalizer()

    questions_answer_reader.test_data_structure()
    questions_answer_reader.test_sort()

    questions_answer_reader.test_get_answer()
    questions_answer_reader.test_process_file("TestResources/LitePerguntasPosSistema.txt")
    questions_answer_reader.dump_map()

    print "--- END OF TESTS ---"