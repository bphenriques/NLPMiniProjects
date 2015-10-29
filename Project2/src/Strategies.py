# -*- coding: utf-8 -

from SimilarityStrategy import SimilarityStrategy
from SimilarityUtil import *


class IdenticalStrategy(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2


class RemoveStopWordsAndStemOnTriggers(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = tok_stem(remove_stop_words(self.normalize_user_input(user_input)))
        trigger = tok_stem(remove_stop_words(self.normalize_user_input(trigger)))

        return user_input == trigger

    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2


class RemoveStopWordsAndStemOnAnswers(SimilarityStrategy):

    def is_user_input_trigger_similar(self, user_input, trigger):
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(self.normalize_user_input(answer1)))
        answer2 = tok_stem(remove_stop_words(self.normalize_user_input(answer2)))

        return answer1 == answer2


class RemoveStopWordsAndStemOnTriggersAndAnswers(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = tok_stem(remove_stop_words(self.normalize_user_input(user_input)))
        trigger = tok_stem(remove_stop_words(self.normalize_user_input(trigger)))

        return user_input == trigger

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(self.normalize_user_input(answer1)))
        answer2 = tok_stem(remove_stop_words(self.normalize_user_input(answer2)))

        return answer1 == answer2


class RemoveStopWordsAndStemOnTriggersAndAnswersMED(SimilarityStrategy):
    _med_user_input_triggers_min = 1
    _med_answers_min = 1

    def __init__(self, user_input_triggers_min_med, answers_min_med):
        description = "%s(%s,%s)" %(self.__class__.__name__, str(user_input_triggers_min_med), str(answers_min_med))
        SimilarityStrategy.__init__(self, description)
        self._med_user_input_triggers_min = user_input_triggers_min_med
        self._med_answers_min = answers_min_med

    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = tok_stem(remove_stop_words(self.normalize_user_input(user_input)))
        trigger = tok_stem(remove_stop_words(self.normalize_user_input(trigger)))

        return med(user_input, trigger) <= self._med_user_input_triggers_min

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(self.normalize_user_input(answer1)))
        answer2 = tok_stem(remove_stop_words(self.normalize_user_input(answer2)))

        return med(answer1, answer2) <= self._med_answers_min
