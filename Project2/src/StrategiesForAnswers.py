# -*- coding: utf-8 -

from SimilarityStrategies import AnswerSimilarityStrategy
from SimilarityUtil import *
from RegexUtil import RegexUtil

###################################################
###################################################
###################################################


class Identical(AnswerSimilarityStrategy):
    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2

###################################################
###################################################
###################################################


class Jaccard(AnswerSimilarityStrategy):
    def __init__(self, threshold, filter):
        AnswerSimilarityStrategy.__init__(self)
        self.__threshold = threshold
        self.__filter = filter
        self.add_arguments_description(threshold, filter)

    def are_answer_similar_enough(self, answer1, answer2):
        if self.__filter:
            answer1, answer2 = remove_stop_words(answer1), remove_stop_words(answer2)
            answer1, answer2 = tok_stem(answer1), tok_stem(answer2)
            answer1, answer2 = RegexUtil.normalize_string(answer1), RegexUtil.normalize_string(answer2)
        else:
            answer1, answer2 = RegexUtil.normalize_string(answer1), RegexUtil.normalize_string(answer2)
        return jaccard_sentence(answer1, answer2) >= self.__threshold


class Dice(AnswerSimilarityStrategy):
    def __init__(self, threshold, filter):
        AnswerSimilarityStrategy.__init__(self)
        self.__threshold = threshold
        self.__filter = filter
        self.add_arguments_description(threshold, filter)

    def are_answer_similar_enough(self, answer1, answer2):
        if self.__filter:
            answer1, answer2 = remove_stop_words(answer1), remove_stop_words(answer2)
            answer1, answer2 = tok_stem(answer1), tok_stem(answer2)
            answer1, answer2 = RegexUtil.normalize_string(answer1), RegexUtil.normalize_string(answer2)
        else:
            answer1, answer2 = RegexUtil.normalize_string(answer1), RegexUtil.normalize_string(answer2)
        return dice_sentence(answer1, answer2) >= self.__threshold

class MED(AnswerSimilarityStrategy):
    def __init__(self, answers_min_med, filter):
        AnswerSimilarityStrategy.__init__(self)
        self._med_answers_min = answers_min_med
        self._filter = filter
        self.add_arguments_description(answers_min_med, filter)

    def are_answer_similar_enough(self, answer1, answer2):
        if self._filter:
            answer1 = RegexUtil.normalize_string(tok_stem(remove_stop_words(answer1)))
            answer2 = RegexUtil.normalize_string(tok_stem(remove_stop_words(answer2)))
        else:
            answer1 = RegexUtil.normalize_string(answer1)
            answer2 = RegexUtil.normalize_string(answer2)

        return med_sentence(answer1, answer2) <= self._med_answers_min

class Braccard(AnswerSimilarityStrategy):
    def __init__(self, tagger, threshold, weight_tag, filter):
        AnswerSimilarityStrategy.__init__(self)
        self.__tagger = tagger
        self.__threshold = threshold
        self.__weight_tag = weight_tag
        self.__filter = filter
        self.add_arguments_description("tagger", threshold, filter)

    def are_answer_similar_enough(self, answer1, answer2):
        if self.__filter:
            answer1, answer2 = remove_stop_words(answer1), remove_stop_words(answer2)

        return custom_jaccard(answer1, answer2, self.__tagger, self.__weight_tag) >= self.__threshold


class YesNoSimilar(AnswerSimilarityStrategy):
    def __init__(self, threshold, weight, measure, filter):
        AnswerSimilarityStrategy.__init__(self)
        self.__threshold = threshold
        self.__weight = weight
        self.__measure = measure
        self.__filter = filter
        self.add_arguments_description(threshold, weight, measure.__name__, filter)

    def are_answer_similar_enough(self, answer1, answer2):
        if self.__filter:
            answer1, answer2 = remove_stop_words(answer1), remove_stop_words(answer2)
            answer1, answer2 = tok_stem(answer1), tok_stem(answer2)
            answer1, answer2 = RegexUtil.normalize_string(answer1), RegexUtil.normalize_string(answer2)
        else:
            answer1, answer2 = RegexUtil.normalize_string(answer1), RegexUtil.normalize_string(answer2)

        return similar_yes_no(answer1, answer2, self.__weight, self.__measure) >= self.__threshold