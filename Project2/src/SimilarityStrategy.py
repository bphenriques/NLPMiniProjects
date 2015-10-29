# -*- coding: utf-8 -

import abc
from RegexUtil import RegexUtil


class SimilarityStrategy(object):
    __metaclass__ = abc.ABCMeta

    description = ""

    def __init__(self, description=None):
        if description is None:
            self.description = self.__class__.__name__
        else:
            self.description = description

    @abc.abstractmethod
    def is_user_input_trigger_similar(self, user_input, trigger):
        return

    @abc.abstractmethod
    def are_answer_similar_enough(self, answer1, answer2):
        return

    def is_user_input_trigger_identical(self, user_input, trigger):
        """

        :param user_input:
        :param trigger:
        :return:
        """
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

    def normalize_user_input(self, user_input):
        """

        :param user_input:
        :return:
        """
        return RegexUtil.normalize_string(user_input)

    def normalize_trigger(self, trigger):
        """

        :param trigger:
        :return:
        """
        return RegexUtil.normalize_string(trigger)

    def normalize_answer(self, answer):
        """

        :param answer:
        :return:
        """
        return answer
