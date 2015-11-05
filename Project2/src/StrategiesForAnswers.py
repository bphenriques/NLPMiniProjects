# -*- coding: utf-8 -

from SimilarityStrategies import AnswerSimilarityStrategy
from SimilarityUtil import *
from RegexUtil import RegexUtil

# ###########################################
# ###########################################
# ###########################################


class Identical(AnswerSimilarityStrategy):
    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2

# ###########################################
# ###########################################
# ###########################################


class RemoveStopWordsAndStem(AnswerSimilarityStrategy):
    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer1)))
        answer2 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer2)))

        return answer1 == answer2

# ###########################################
# ###########################################
# ###########################################


# in short MegaStrategy
class RemoveStopWordsAndStemMED(AnswerSimilarityStrategy):
    _med_answers_min = 1

    def __init__(self, answers_min_med):
        AnswerSimilarityStrategy.__init__(self)

        self.add_arguments_description(answers_min_med)
        self._med_answers_min = answers_min_med

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer1)))
        answer2 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer2)))

        return med(answer1, answer2) <= self._med_answers_min


# ###########################################
# ###########################################
# ###########################################


class Braccard(AnswerSimilarityStrategy):
    __tagger = None
    __threshold = 0

    def __init__(self, tagger, threshold = 0.8):
        AnswerSimilarityStrategy.__init__(self, )
        self.__tagger = tagger
        self.__threshold = threshold
        self.add_arguments_description(threshold)

    def are_answer_similar_enough(self, answer1, answer2):
        s1 = RegexUtil.normalize_string(answer1)
        s2 = RegexUtil.normalize_string(answer2)
        return custom_jaccard(s1, s2, self.__tagger) >= self.__threshold