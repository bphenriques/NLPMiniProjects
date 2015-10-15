import TestsUtil
from AnnotationCheck import AnnotationCheck
from AnswerPicker import AnswerPicker


class AnnotationCheckTests(AnnotationCheck):
    _answer_picker = AnswerPicker()
    _annotation_check = None

    def __init__(self, corpus_path, annotation_file_path):
        AnnotationCheck.__init__(self, annotation_file_path)
        self._answer_picker.process_file(corpus_path)

    def __aux_test_stats(self, questions_file, expected_value):
        assert expected_value == self.evaluate_accuracy(self._answer_picker, questions_file, 20)

    def test_stats(self):
        """
        Test 1
        """
        self.__aux_test_stats("TestResources/Perguntas.txt", (float(1)/3))

    def see_stats(self):
        """
        Test 1
        """

        print self.evaluate_accuracy(self._answer_picker, "TestResources/banana.txt", 20)




if __name__ == "__main__":
    annotation_check_tests = AnnotationCheckTests("TestResources/PerguntasPosSistema.txt", "TestResources/AnotadoAll.txt")

    tests = [
        annotation_check_tests.test_stats,
        annotation_check_tests.see_stats
    ]

    TestsUtil.run_tests(tests)
