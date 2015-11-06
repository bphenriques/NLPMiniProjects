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
        answer1 = RegexUtil.normalize_string(tok_stem(remove_stop_words(answer1)))
        answer2 = RegexUtil.normalize_string(tok_stem(remove_stop_words(answer2)))

        return answer1 == answer2

# ###########################################
# ###########################################
# ###########################################


# in short MegaStrategy
class RemoveStopWordsAndStemMED(AnswerSimilarityStrategy):
    def __init__(self, answers_min_med):
        AnswerSimilarityStrategy.__init__(self)

        self.add_arguments_description(answers_min_med)
        self._med_answers_min = answers_min_med

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = RegexUtil.normalize_string(tok_stem(remove_stop_words(answer1)))
        answer2 = RegexUtil.normalize_string(tok_stem(remove_stop_words(answer2)))

        return med(answer1, answer2) <= self._med_answers_min


# ###########################################
# ###########################################
# ###########################################

# TODO BRACCARD COM STEM
class Braccard(AnswerSimilarityStrategy):
    def __init__(self, tagger, threshold = 0.8):
        AnswerSimilarityStrategy.__init__(self)
        self.__tagger = tagger
        self.__threshold = threshold
        self.add_arguments_description("tagger", threshold)

    def are_answer_similar_enough(self, answer1, answer2):
        s1 = RegexUtil.normalize_string(answer1)
        s2 = RegexUtil.normalize_string(answer2)
        return custom_jaccard(s1, s2, self.__tagger) >= self.__threshold


class Jaccard(AnswerSimilarityStrategy):
    def __init__(self, threshold = 0.8):
        AnswerSimilarityStrategy.__init__(self)
        self.__threshold = threshold
        self.add_arguments_description(threshold)

    def are_answer_similar_enough(self, answer1, answer2):
        s1, s2 = RegexUtil.normalize_string(answer1), RegexUtil.normalize_string(answer2)
        return jaccard_sentence(s1, s2) >= self.__threshold


class Dice(AnswerSimilarityStrategy):
    def __init__(self, threshold = 0.8):
        AnswerSimilarityStrategy.__init__(self)
        self.__threshold = threshold
        self.add_arguments_description(threshold)

    def are_answer_similar_enough(self, answer1, answer2):
        s1, s2 = RegexUtil.normalize_string(answer1), RegexUtil.normalize_string(answer2)
        return dice_sentence(s1, s2) >= self.__threshold

class JaccardStem(AnswerSimilarityStrategy):
    def __init__(self, threshold = 0.8):
        AnswerSimilarityStrategy.__init__(self)
        self.__threshold = threshold
        self.add_arguments_description(threshold)

    def are_answer_similar_enough(self, answer1, answer2):
        s1, s2 = remove_stop_words(answer1), remove_stop_words(answer2)
        s1, s2 = tok_stem(s1), tok_stem(s2)
        s1, s2 = RegexUtil.normalize_string(s1), RegexUtil.normalize_string(s2)
        return jaccard_sentence(s1, s2) >= self.__threshold


class DiceStem(AnswerSimilarityStrategy):
    def __init__(self, threshold = 0.8):
        AnswerSimilarityStrategy.__init__(self)
        self.__threshold = threshold
        self.add_arguments_description(threshold)

    def are_answer_similar_enough(self, answer1, answer2):
        s1, s2 = remove_stop_words(answer1), remove_stop_words(answer2)
        s1, s2 = tok_stem(s1), tok_stem(s2)
        s1, s2 = RegexUtil.normalize_string(s1), RegexUtil.normalize_string(s2)
        return dice_sentence(s1, s2) >= self.__threshold


class YesNoSimilar(AnswerSimilarityStrategy):
    def __init__(self, threshold = 0.8):
        AnswerSimilarityStrategy.__init__(self)
        self.__threshold = threshold
        self.add_arguments_description(threshold)

    def are_answer_similar_enough(self, answer1, answer2):
        s1, s2 = remove_stop_words(answer1), remove_stop_words(answer2)
        s1, s2 = tok_stem(s1), tok_stem(s2)
        s1, s2 = RegexUtil.normalize_string(s1), RegexUtil.normalize_string(s2)
        return similar_yes_no(s1, s2) >= self.__threshold