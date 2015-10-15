# -*- coding: utf-8 -
import re
import os.path
import string
from RegexUtil import RegexUtil
from AnswerPicker import AnswerPicker


class AnnotationCheck:
    POSITIVE_CHAR = 'y'
    NEGATIVE_CHAR = 'n'
    MAYBE_CHAR = 'm'

    _annotation_file_path = None
    _user_input_regex_prefix = "User Input" + r"[\s]*" + "-" + r"[\s]*"
    _answer_regex_prefix = r"[\s]*" + "A" + r"[\s]*" + "-" + r"[\s]*"
    _answer_regex_sufix = None
    _annotation_separator_regex = r"[\s]*" + ":" + r"[\s]*"

    def __init__(self, annotation_file_path):
        """
        :param annotation_file_path:
        """
        if not os.path.exists(annotation_file_path):
            print "File not found"
            raise Exception

        self._annotation_file_path = annotation_file_path
        self._answer_regex_sufix = self._annotation_separator_regex + "[" + self.POSITIVE_CHAR + self.NEGATIVE_CHAR + self.MAYBE_CHAR + "]"

    def evaluate_accuracy(self, answer_picker, questions_file_path, max_n_answers):
        if not os.path.exists(questions_file_path):
            print "Questions File not found"
            raise Exception

        answers_list = self._evaluate(answer_picker, questions_file_path, max_n_answers)
        return self._accuracy(answers_list)

    def _evaluate(self, answer_picker, questions_file_path, max_n_answers):
        """
        Bla bla bla
        :param answer_picker:
        :param questions_file_path:
        :param max_n_answers:
        :return:
        """

        answers_list = list()
        with open(questions_file_path) as questionFile:
            for question in questionFile:
                answer = answer_picker.get_answer(question)

                if (answer == AnswerPicker.INVALID_USER_INPUT) or (answer == AnswerPicker.TRIGGER_NOT_FOUND):
                    annotation = 'n'
                else:
                    annotation = self._get_annotation(question, answer, max_n_answers)

                answers_list.append(annotation)
            questionFile.close()
        return answers_list

    def _get_annotation(self, user_input, answer, max_n_answers):
        """
        Gets the corresponding annotation from the answer given an user-input

        To simplify and since it wasn't required, the user_input is not normalized,
        i.e., keep case, keep diacritric and keep ponctuation

        :param user_input:
        :param answer:
        :param max_n_answers:
        :return: the annotation
        """

        file_in = open(self._annotation_file_path)

        # regex to find specific user_input in the file
        match_question_regex = self._user_input_regex_prefix + user_input

        line = file_in.readline()
        while line:
            match_question = re.search(match_question_regex, line)
            if match_question is not None:
                for i in range(0, max_n_answers):
                    answer_line = file_in.readline()
                    # find specific answer
                    match_answer = re.search(answer + self._answer_regex_sufix, answer_line)
                    if match_answer is not None:
                        # Remove A - Bla bla bla and keep only the annotation
                        not_annotation_regex = self._answer_regex_prefix + answer + self._annotation_separator_regex
                        annotation = re.sub(not_annotation_regex, '', match_answer.string).strip(string.whitespace)

                        file_in.close()
                        return annotation
            line = file_in.readline()

    def _accuracy(self, answers):
        """
        :param answers:
        :param positive_char:
        :return:
        """

        if len(answers) == 0: return 0

        tp = answers.count(self.POSITIVE_CHAR)
        return float(tp) / len(answers)
