# -*- coding: utf-8 -

import abc
from RegexUtil import RegexUtil
import SimilarityUtil


class SimilarityStrategy(object):
    __metaclass__ = abc.ABCMeta

    description = ""

    def __init__(self, description=None):
        if description is None:
            self.description = self.__class__.__name__
        else:
            self.description = description

        self.add_arguments_description()

    def add_arguments_description(self, *args):
        self.description = self.__class__.__name__ + "("
        for i in range(0, len(args)):
            self.description += str(args[i])
            if i != len(args) - 1:
                self.description += ", "

        self.description += ")"


class TriggerSimilarityStrategy(SimilarityStrategy):
    __metaclass__ = abc.ABCMeta

    def __init__(self, description=None):
        SimilarityStrategy.__init__(self, description)

    @abc.abstractmethod
    def is_user_input_trigger_similar(self, user_input, trigger):
        return

    def normalize_trigger(self, trigger):
        return RegexUtil.normalize_string(SimilarityUtil.filter_non_interrogative_sentence(trigger))

    def normalize_user_input(self, user_input):
        return RegexUtil.normalize_string(user_input)

    def is_user_input_trigger_identical(self, user_input, trigger):
        return RegexUtil.normalize_string(user_input) == RegexUtil.normalize_string(trigger)

class AnswerSimilarityStrategy(SimilarityStrategy):
    __metaclass__ = abc.ABCMeta

    def __init__(self, description=None):
        SimilarityStrategy.__init__(self, description)

    @abc.abstractmethod
    def are_answer_similar_enough(self, answer1, answer2):
        return

    def normalize_answer(self, answer):
        return answer






