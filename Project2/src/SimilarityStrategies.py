# -*- coding: utf-8 -

import abc
from RegexUtil import RegexUtil

class SimilarityStrategy(object):
    """
    Abstract class for defining strategy design pattern
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, description=None):
        """
        :param description: default is the name of the class
        """
        if description is None:
            self.description = self.__class__.__name__
        else:
            self.description = description

        self.add_arguments_description()

    def add_arguments_description(self, *args):
        """
        Changes self.description field with format <className(arg1, arg2,...,argn)>
        :param args: list of arguments
        """
        self.description = self.__class__.__name__ + "("
        for i in range(0, len(args)):
            self.description += str(args[i])
            if i != len(args) - 1:
                self.description += ", "

        self.description += ")"


class TriggerSimilarityStrategy(SimilarityStrategy):
    """
    Abstract class for defining strategy for comparing user input and triggers
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, description=None):
        SimilarityStrategy.__init__(self, description)

    @abc.abstractmethod
    def is_user_input_trigger_similar(self, user_input, trigger):
        """
        Return true if user_input and trigger are similar enough, false if not
        :param user_input:
        :param trigger:
        :return: true if are similar enough
        """
        return

    def is_user_input_trigger_identical(self, user_input, trigger):
        return RegexUtil.normalize_string(user_input) == RegexUtil.normalize_string(trigger)

class AnswerSimilarityStrategy(SimilarityStrategy):
    """
    Abstract class for defining strategy for comparing answers
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, description=None):
        SimilarityStrategy.__init__(self, description)

    @abc.abstractmethod
    def are_answer_similar_enough(self, answer1, answer2):
        """
        Returns true if answer1 and answer2 are similar enough, false if not.
        :param answer1:
        :param answer2:
        :return: true if are similar enough
        """
        return






