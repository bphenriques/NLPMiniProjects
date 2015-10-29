# -*- coding: utf-8 -*-

from AnswerPicker import AnswerPicker
from AnswerPicker import AnswerPickerAnswerResult
from SimilarityStrategy import  SimilarityStrategy
from UserInputTriggerAnswerReader import UserInputTriggerAnswerReader
from Tests import TestsUtil

class TestAnswerPicker(AnswerPicker):
    def test_trigger_inexistent(self):
        self.clear()

        # added new question but trigger does not match
        self.process_user_input_answer("Question3", "trigger", "Response2")

        answers = self.get_answers("Question3")
        assert answers is not None and len(answers) == 0
        answer = self.get_answer("Question3")
        assert answer == AnswerPickerAnswerResult.TRIGGER_NOT_FOUND

    def test_wrong_user_input(self):
        self.clear()

        # Find non-existent trigger
        answers = self.get_answers("Bla")
        assert answers is None
        answer = self.get_answer("Bla")
        assert answer == AnswerPickerAnswerResult.INVALID_USER_INPUT

    def test_answer_frequency(self):
        self.clear()

        # Test one addition
        self.process_user_input_answer("Question1", "Question1", "Response1")
        assert(len(self.get_answers("Question1")) == 1)

        # Test multiple responses for same question
        self.process_user_input_answer("Question2", "Question2", "Response1")
        self.process_user_input_answer("Question2", "Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)

        # Test same response for same question and therefore should increment
        self.process_user_input_answer("Question2", "Question2", "Response2")
        assert(len(self.get_answers("Question2")) == 2)
        answers = self.get_answers("Question2")
        assert answers is not None
        answer = self._find_answer(answers, self._similarity_strategy.normalize_answer("Response2"))
        assert answer is not None
        assert answer[0] == self._similarity_strategy.normalize_answer("Response2")
        assert answer[1] == 2

    def test_sort(self):
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response1")
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2")
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")  # Response3 : 2
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")  # Response3 : 3
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response3")  # Response3 : 4
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2")  # Response2 : 2
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response1")  # Response1 : 2
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response2")  # Response2 : 3
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response4")  # Response4 : 1
        self.process_user_input_answer("TestQuestion2", "TestQuestion2", "Response5")  # Response5 : 1

        # Tests if the  answers stored are sorted from the most frequent to the least frequent
        answers = self.get_answers("TestQuestion2")
        assert answers[0][0] == self._similarity_strategy.normalize_answer("Response3")
        assert answers[1][0] == self._similarity_strategy.normalize_answer("Response2")
        assert answers[2][0] == self._similarity_strategy.normalize_answer("Response1")
        assert answers[3][0] == self._similarity_strategy.normalize_answer("Response5") or \
               answers[3][0] == self._similarity_strategy.normalize_answer("Response4")
        assert answers[4][0] == self._similarity_strategy.normalize_answer("Response5") or \
               answers[4][0] == self._similarity_strategy.normalize_answer("Response4")

    def test_get_answer(self):
        self.clear()
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response1")
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")  # Response3 : 2
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")  # Response3 : 3
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")  # Response3 : 4
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")  # Response2 : 2
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response1")  # Response1 : 2
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")  # Response2 : 3
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response4")  # Response4 : 1
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response5")  # Response5 : 1

        # Response3 is most frequent: 4
        assert self.get_answer("TestQuestion1") == self._similarity_strategy.normalize_answer("Response3")

        # changing the leadership
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")  # Response2 : 4
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response2")  # Response2 : 5

        # Response2 is most frequent: 5
        assert self.get_answer("TestQuestion1") == self._similarity_strategy.normalize_answer("Response2")

        # Response3 and Response2 are 5 (draw)
        self.process_user_input_answer("TestQuestion1", "TestQuestion1", "Response3")  # Response3 : 5
        assert self.get_answer("TestQuestion1") == self._similarity_strategy.normalize_answer("Response2") or \
               self.get_answer("TestQuestion1") == self._similarity_strategy.normalize_answer("Response3")

    def test_normalizer(self):
        self.clear()

        self.process_user_input_answer("TestQuestion3", "TestQuestion3", "Response1")
        self.process_user_input_answer("TestQuestion3", "TéstQuestion3", "Response2")
        self.process_user_input_answer("TestQuestion3", "TéstQuestion3.", "Response3")
        self.process_user_input_answer("TestQuestion3", "Tést,Quèstíõn3.", "Response4")
        self.process_user_input_answer("TestQuestion3", "Tèst,Questiôn3.", "Response5")
        self.process_user_input_answer("TestQuestion3", "Tést,Question3.", "Response6")
        self.process_user_input_answer("TestQuestion3", "Tést,QUESTION3.", "Response7")
        self.process_user_input_answer("TestQuestion3", "Tést,QUESTION3.\n", "Response8")
        self.process_user_input_answer("TestQuestion3", "Tést!,QUESTION3.\n", "Response9")
        self.process_user_input_answer("TestQuestion3", "Tést!,QU:ES;TI,ON?3.\n", "Response10")
        self.process_user_input_answer("TestQuestion3", "Tést!,QU:ES;TI,ON?3.\n", "Response11")
        self.process_user_input_answer("TestQuestion3", "Tést!,\"QU:ES;TI,O\"N?3.\r\n", "Response12")
        self.process_user_input_answer("TestQuestion3", "Té)s(t!,\"QU:E(S;TI,O\"N?3.\n", "Response13")
        self.process_user_input_answer("TestQuestion3", "Té)s(t!,\"QU:E(S;TÍ,Õ\"N?3.\n", "Response13")

        assert len(self.get_answers("TestQuestion3")) == 13

    def test_process__lite_file(self):
        self.clear()
        self._file_reader.process_file("TestResources/LitePerguntasPosSistema.txt", self.process_user_input_answer)

        assert self.number_matched_user_input() == 3
        assert len(self.get_answers("Tens filhos?")) == 12
        assert self.get_answer("Tens filhos?") == u"Não."

    def test_process_big_file(self):
        self.clear()
        self._file_reader.process_file("TestResources/PerguntasPosSistema.txt", self.process_user_input_answer)

        # The following question has no triggers that are similar to the user input
        assert self.get_answer("A tua familia é numerosa?") == AnswerPickerAnswerResult.TRIGGER_NOT_FOUND

        # Non existent at all
        assert self.get_answer("I DONT EXIST?") == AnswerPickerAnswerResult.INVALID_USER_INPUT

        # There are many similar triggers with this user_input
        assert self.get_answer("Tens filhos?") == u"Não."
        assert self.get_answer("tens filhos?") == AnswerPickerAnswerResult.INVALID_USER_INPUT

    def test_delete_similar_triggers_after_identical_trigger(self):
        self.clear()

        self._similarity_strategy = StrategyTriggersAlwaysSimilar()

        # Tailored made file
        self._file_reader.process_file("TestResources/Lite2ndPerguntasPosSistema.txt", self.process_user_input_answer)

        answers1 = self.get_answers("A tua familia é numerosa?")
        assert len(answers1) == 1
        assert self.get_answer("A tua familia é numerosa?") == u"Olha, eu estou apenas a começar a minha vida, de volta juntos."

        answers2 = self.get_answers("Aceitas tomar café?")
        assert len(answers2) == 16
        assert self.get_answer("Aceitas tomar café?") == u"Não, obrigado."

        answers3 = self.get_answers("Tens filhos?")
        assert len(answers3) == 12
        assert self.get_answer("Tens filhos?") == u"Não."

        answers4 = self.get_answers("Como se chama a tua mãe?")
        assert len(answers4) == 1
        assert self.get_answer("Como se chama a tua mãe?") == u"Mãmã"

    def test_similar_answers(self):
        self.clear()

        self._similarity_strategy = StrategyEverythingIsSimilar()

        # Tailored made file
        self._file_reader.process_file("TestResources/Lite2ndPerguntasPosSistema.txt", self.process_user_input_answer)

        # only one possible answer with probability 20 (number of answers in the file)
        answers2 = self.get_answers("Aceitas tomar café?")
        assert len(answers2) == 1
        assert answers2[0][1] == 20
        # it's always the first answer found that is stored. The following ones are not stored
        assert self.get_answer("Aceitas tomar café?") == u"Não, obrigada."


class StrategyTriggersAlwaysSimilar(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return True

    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2


class StrategyEverythingIsSimilar(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return True

    def are_answer_similar_enough(self, answer1, answer2):
        return True


if __name__ == '__main__':
    questions_answer_reader = TestAnswerPicker(UserInputTriggerAnswerReader())

    tests = [
        questions_answer_reader.test_trigger_inexistent,
        questions_answer_reader.test_wrong_user_input,
        questions_answer_reader.test_answer_frequency,
        questions_answer_reader.test_normalizer,
        questions_answer_reader.test_sort,
        questions_answer_reader.test_get_answer,
        questions_answer_reader.test_process__lite_file,
        questions_answer_reader.test_process_big_file,
        questions_answer_reader.test_delete_similar_triggers_after_identical_trigger,
        questions_answer_reader.test_similar_answers
    ]

    TestsUtil.run_tests(tests)