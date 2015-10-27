# -*- coding: utf-8 -*-

from UserInputTriggerAnswerReader import UserInputTriggerAnswerReader
import TestsUtil


class TestUserInputTriggerAnswerReader(UserInputTriggerAnswerReader):
    """
    Test class for AnswerPicker
    """

    def test_answer_regex(self):
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


if __name__ == '__main__':
    user_input_trigger_answer_tests = TestUserInputTriggerAnswerReader()

    tests = [
        user_input_trigger_answer_tests.test_answer_regex,
        user_input_trigger_answer_tests.test_trigger_regex,
        user_input_trigger_answer_tests.test_user_input_regex
    ]

    TestsUtil.run_tests(tests)

