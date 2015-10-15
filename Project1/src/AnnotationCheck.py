# -*- coding: utf-8 -
import re
import os.path
import string
from RegexUtil import RegexUtil
from AnswerPicker import AnswerPickerAnswerResult


class AnnotationCheck:
    POSITIVE_CHAR = 'y'
    NEGATIVE_CHAR = 'n'
    MAYBE_CHAR = 'm'

    _annotation_file_path = None
    _user_input_regex_prefix = "^[\s]*User Input" + "[\s]*" + "-" + "[\s]*"
    _answer_regex_prefix = "^[\s]*A" + "[\s]*" + "-" + "[\s]*"
    _answer_regex_sufix = None
    _annotation_separator_regex = "[\s]*" + ":" + "[\s]*"

    def __init__(self, annotation_file_path):
        """
        :param annotation_file_path:
        """
        if not os.path.exists(annotation_file_path):
            print "File not found"
            raise Exception

        self._annotation_file_path = annotation_file_path
        self._answer_regex_sufix = self._annotation_separator_regex + "[" + self.POSITIVE_CHAR + self.NEGATIVE_CHAR + self.MAYBE_CHAR + "][\s]*$"

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
                question = RegexUtil.custom_strip(question)
                answer = answer_picker.get_answer(question)

                if (answer == AnswerPickerAnswerResult.INVALID_USER_INPUT) or (answer == AnswerPickerAnswerResult.TRIGGER_NOT_FOUND):
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
        line = file_in.readline()
        while line:
            # Search User Input: in the beginning of the line
            sole_question = re.sub(self._user_input_regex_prefix, '', line)
            sole_question = re.sub("[\s]*$", '', sole_question)

            if sole_question == user_input:
                for i in range(0, max_n_answers):
                    answer_line = file_in.readline().decode('utf-8')

                    # Getting answer by removing prefix and sufix
                    potential_answer = re.sub(self._answer_regex_prefix, '', answer_line)
                    potential_answer = re.sub(self._answer_regex_sufix, '', potential_answer)

                    if potential_answer == answer:
                        splits_separator = re.split(self._annotation_separator_regex, answer_line)
                        if len(splits_separator) == 0: continue
                        file_in.close()

                        annotation = splits_separator[len(splits_separator) - 1]
                        annotation = annotation.strip(string.whitespace) # remove carriage and newlines

                        return annotation

            line = file_in.readline()

        # if user question is not found
        return self.NEGATIVE_CHAR

    def _accuracy(self, answers):
        """
        :param answers:
        :param positive_char:
        :return:
        """
        if len(answers) == 0: return 0

        tp = answers.count(self.POSITIVE_CHAR)
        return float(tp) / len(answers)
