# -*- coding: utf-8 -

import re
import os.path
import string
from RegexUtil import RegexUtil
from AnswerPicker import AnswerPickerAnswerResult


class AnnotationCheck:
    """
    AnnotationChecker. Allows evaluating accuracy of a set of User_Questions and answers
    """

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
        Constructor. If the annotation_file_path doesn't exist an exception is thrown

        :param annotation_file_path: the file path to the annotation
        """
        if not os.path.exists(annotation_file_path):
            print "File not found"
            raise Exception

        self._annotation_file_path = annotation_file_path
        self._answer_regex_sufix = self._annotation_separator_regex + "[" + self.POSITIVE_CHAR + self.NEGATIVE_CHAR + self.MAYBE_CHAR + "][\s]*$"

    def evaluate_accuracy(self, answer_picker, questions_file_path, max_n_answers):
        """
        Determines the accuracy of a AnswerPicker given a list of questions

        :param answer_picker: instance of AnswerPicker with the corpus already studied
        :param questions_file_path: source of questions
        :param max_n_answers: max number of answers to look for
        :return: accuracy of the answer_picker
        """

        if not os.path.exists(questions_file_path):
            print "Questions File not found"
            raise Exception

        # list of y, n or m
        answers_stats_list = self._evaluate(answer_picker, questions_file_path, max_n_answers)
        return self._accuracy(answers_stats_list)

    def _evaluate(self, answer_picker, questions_file_path, max_n_answers):
        answers_list = list()
        with open(questions_file_path) as questionFile:
            for question in questionFile:
                # remove - and whitespace
                question = RegexUtil.custom_strip(question)
                answer = answer_picker.get_answer(question)

                # check if input is invalid or if there is no possible answer
                if answer == AnswerPickerAnswerResult.INVALID_USER_INPUT or AnswerPickerAnswerResult.TRIGGER_NOT_FOUND == answer:
                    annotation = 'n'
                else:
                    annotation = self._get_annotation(question, answer, max_n_answers)

                # add to the list for future analysis
                answers_list.append(annotation)
            questionFile.close()
        return answers_list

    def _get_annotation(self, user_input, answer, max_n_answers):
        file_in = open(self._annotation_file_path)

        line = file_in.readline()
        while line:
            # Search User Input: in the beginning of the line
            sole_question = re.sub(self._user_input_regex_prefix, '', line)
            sole_question = re.sub("[\s]*$", '', sole_question)

            if sole_question == user_input:
                for i in range(0, max_n_answers):
                    # answer is in utf-8 therefore we convert the line to utf-8 as well
                    answer_line = file_in.readline().decode('utf-8')

                    # Getting answer by removing prefix and sufix
                    potential_answer = re.sub(self._answer_regex_prefix, '', answer_line)
                    potential_answer = re.sub(self._answer_regex_sufix, '', potential_answer)

                    if potential_answer == answer:
                        # split the sentence with the separator
                        splits_separator = re.split(self._annotation_separator_regex, answer_line)
                        if len(splits_separator) == 0: continue
                        file_in.close()

                        annotation = splits_separator[len(splits_separator) - 1]
                         # remove carriage and newlines
                        annotation = annotation.strip(string.whitespace).lower()

                        return annotation

            line = file_in.readline()

        # if user question is not found
        return self.NEGATIVE_CHAR

    def _accuracy(self, answers):
        if len(answers) == 0: return 0

        tp = answers.count(self.POSITIVE_CHAR)
        return float(tp) / len(answers)
