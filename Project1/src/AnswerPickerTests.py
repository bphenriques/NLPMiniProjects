# -*- coding: utf-8 -*-

from AnswerPicker import AnswerPicker
from AnswerPicker import AnswerPickerAnswerResult
import TestsUtil


class TestAnswerPicker(AnswerPicker):
    """
    Test class for AnswerPicker
    """

    def test_answer_regex(self):
        """
        Tests answer regex. If fails, an exception is thrown.
        """

        test_in = "A - (ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ). Derp. Não estou a dizer coisa com coisa"
        expected = "(ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ). Derp. Não estou a dizer coisa com coisa"
        assert expected == self._read_answer(test_in)

        test_in = "T - (ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ). Derp. Não estou a dizer coisa com coisa"
        assert self._read_answer(test_in) is None

        test_in = "A -    STUFF   "
        expected = "STUFF"
        assert expected == self._read_answer(test_in)

        test_in = "A -  \t  STUFF  \t "
        expected = "STUFF"
        assert expected == self._read_answer(test_in)

        test_in = "A -  STUFF\n"
        expected = "STUFF"
        assert expected == self._read_answer(test_in)

        test_in = "A -  STUFF\r\n"
        expected = "STUFF"
        assert expected == self._read_answer(test_in)


    def test_trigger_regex(self):
        """
        Tests trigger regex. If fails, an exception is thrown.
        """

        test_in = "T - (ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ). Derp. Não estou a dizer coisa com coisa"
        expected = "(ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ). Derp. Não estou a dizer coisa com coisa"
        assert expected == self._read_trigger(test_in)

        test_in = "A - (ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ). Derp. Não estou a dizer coisa com coisa"
        assert self._read_trigger(test_in) is None

        test_in = "T -    STUFF   "
        expected = "STUFF"
        assert expected == self._read_trigger(test_in)

        test_in = "T -  \t  STUFF  \t "
        expected = "STUFF"
        assert expected == self._read_trigger(test_in)

        test_in = "T -  STUFF\n"
        expected = "STUFF"
        assert expected == self._read_trigger(test_in)

        test_in = "T -  STUFF\r\n"
        expected = "STUFF"
        assert expected == self._read_trigger(test_in)

    def test_user_input_regex(self):
        """
        Tests user input regex. If fails, an exception is thrown.
        """

        assert "Bla bla bla" == self._read_user_input("User Input: Bla bla bla")
        assert self._read_user_input("GIBBERISH") is None
        assert self._read_user_input("user input: asdhasdh") is None

        test_in = "User Input:    STUFF   "
        expected = "STUFF"
        assert expected == self._read_user_input(test_in)

        test_in = "User Input:  \t STUFF  \t "
        expected = "STUFF"
        assert expected == self._read_user_input(test_in)

        test_in = "User Input:  STUFF\n"
        expected = "STUFF"
        assert expected == self._read_user_input(test_in)

        test_in = "User Input:  STUFF\r\n"
        expected = "STUFF"
        assert expected == self._read_user_input(test_in)

    def test_trigger_inexistent(self):
        """
        Tests inexistent trigger for a given user input
        """

        self.clear()

        # added new question but trigger does not match
        self._process_user_input_answer("Question3", "trigger", "Response2")

        answers = self.get_answers("Question3")
        assert answers is not None and len(answers) == 0
        answer = self.get_answer("Question3")
        assert answer == AnswerPickerAnswerResult.TRIGGER_NOT_FOUND

    def test_wrong_user_input(self):
        """
        Tests wrong user_input
        """

        self.clear()

        # Find non-existent trigger
        answers = self.get_answers("Bla")
        assert answers is None
        answer = self.get_answer("Bla")
        assert answer == AnswerPickerAnswerResult.INVALID_USER_INPUT

    def test_answer_frequency(self):
        """
        Tests answer frequency. Adds several triggers and answers and verifies if the insertion are correct and if
        the frequency of those same answers are being updated as expected
        """

        self.clear()

        # Test one addition
        self._process_user_input_answer("Question1", "Question1", "Response1")
        assert(len(self.get_answers("Question1")) == 1)

        # Test multiple responses for same question
        self._process_user_input_answer("Question2", "Question2", "Response1")
        self._process_user_input_answer("Question2", "Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)

        # Test same response for same question and therefore should increment
        self._process_user_input_answer("Question2", "Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)
        answers = self.get_answers("Question2")
        assert answers is not None
        answer = self._find_answer(answers, self.normalize_answer("Response2"))
        assert answer is not None
        assert answer[0] == self.normalize_answer("Response2")
        assert answer[1] == 2

    def test_sort(self):
        """
        Tests if the  answers stored are sorted from the most frequent to the least frequent
        """

        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response1")
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2")
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")  # Response3 : 2
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")  # Response3 : 3
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")  # Response3 : 4
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2")  # Response2 : 2
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response1")  # Response1 : 2
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2")  # Response2 : 3
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response4")  # Response4 : 1
        self._process_user_input_answer("TestQuestion2", "TestQuestion2", "Response5")  # Response5 : 1

        answers = self.get_answers("TestQuestion2")
        assert answers[0][0] == self.normalize_answer("Response3")
        assert answers[1][0] == self.normalize_answer("Response2")
        assert answers[2][0] == self.normalize_answer("Response1")
        assert answers[3][0] == self.normalize_answer("Response5") or \
               answers[3][0] == self.normalize_answer("Response4")
        assert answers[4][0] == self.normalize_answer("Response5") or \
               answers[4][0] == self.normalize_answer("Response4")

    def test_get_answer(self):
        """
        Tests if it is return the most frequent answer
        """

        self.clear()
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response1")
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")  # Response3 : 2
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")  # Response3 : 3
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")  # Response3 : 4
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")  # Response2 : 2
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response1")  # Response1 : 2
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")  # Response2 : 3
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response4")  # Response4 : 1
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response5")  # Response5 : 1

        # Response3 is most frequent: 4
        assert self.get_answer("TestQuestion1") == self.normalize_answer("Response3")

        # changing the leadership
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")  # Response2 : 4
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")  # Response2 : 5

        # Response2 is most frequent: 5
        assert self.get_answer("TestQuestion1") == self.normalize_answer("Response2")

        # Response3 and Response2 are 5 (draw)
        self._process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")  # Response3 : 5
        assert self.get_answer("TestQuestion1") == self.normalize_answer("Response2") or \
               self.get_answer("TestQuestion1") == self.normalize_answer("Response3")

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

    def test_process__lite_file(self, file_name = "TestResources/LitePerguntasPosSistema.txt"):
        """
        Tests a lite file
        """
        self.clear()
        self.process_file(file_name)
        assert self.number_matched_user_input() == 3
        assert len(self.get_answers("Tens filhos?")) == 12
        assert self.get_answer("Tens filhos?") == u"Não."

    def test_process_big_file(self, file_name = "TestResources/PerguntasPosSistema.txt"):
        """
        Tests big file
        """
        self.clear()
        self.process_file(file_name)

        # The following question has no triggers that are similar to the user input
        assert self.get_answer("A tua familia é numerosa?") == AnswerPickerAnswerResult.TRIGGER_NOT_FOUND

        #Non existent at all
        assert self.get_answer("I DONT EXIST?") == AnswerPickerAnswerResult.INVALID_USER_INPUT

        #There are many similar triggers with this user_input
        assert self.get_answer("Tens filhos?") == u"Não."
        assert self.get_answer("tens filhos?") == AnswerPickerAnswerResult.INVALID_USER_INPUT


if __name__ == '__main__':
    questions_answer_reader = TestAnswerPicker()

    tests = [
        questions_answer_reader.test_answer_regex,
        questions_answer_reader.test_trigger_regex,
        questions_answer_reader.test_user_input_regex,
        questions_answer_reader.test_trigger_inexistent,
        questions_answer_reader.test_wrong_user_input,
        questions_answer_reader.test_answer_frequency,
        questions_answer_reader.test_normalizer,
        questions_answer_reader.test_sort,
        questions_answer_reader.test_get_answer,
        questions_answer_reader.test_process__lite_file,
        questions_answer_reader.test_process_big_file
    ]

    TestsUtil.run_tests(tests)

