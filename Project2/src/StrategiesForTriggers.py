# -*- coding: utf-8 -

from RegexUtil import RegexUtil
from SimilarityStrategies import TriggerSimilarityStrategy
from SimilarityUtil import *


class IdenticalNormalized(TriggerSimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return RegexUtil.normalize_string(user_input) == RegexUtil.normalize_string(filter_non_interrogative_sentence(trigger))


class RemoveStopWordsAndStem(TriggerSimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = RegexUtil.normalize_string(tok_stem(remove_stop_words(user_input)))
        trigger = RegexUtil.normalize_string(filter_non_interrogative_sentence(tok_stem(remove_stop_words(trigger))))

        return user_input == trigger


class RemoveStopWordsAndStemMED(TriggerSimilarityStrategy):
    def __init__(self, user_input_triggers_min_med):
        TriggerSimilarityStrategy.__init__(self)

        self.add_arguments_description(user_input_triggers_min_med)
        self._med_user_input_triggers_min = user_input_triggers_min_med

    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = RegexUtil.normalize_string(tok_stem(remove_stop_words(user_input)))
        trigger = RegexUtil.normalize_string(filter_non_interrogative_sentence(tok_stem(remove_stop_words(trigger))))

        return med(user_input, trigger) <= self._med_user_input_triggers_min


# Applys extra filter on gramatical category
class MegaStrategyFiltering(TriggerSimilarityStrategy):
    # Measure is dice_sentence of jaccard_sentence
    def __init__(self, tagger, measure, threeshold, filter_tag_triggers=None):
        TriggerSimilarityStrategy.__init__(self)

        self._tagger = tagger
        self._measure = measure
        self._threeshold = threeshold

        if filter_tag_triggers is not None:
            self._tags_to_filter_triggers = filter_tag_triggers
        else:
            self._tags_to_filter_triggers = ["n", "in", "prop", "art", "pron-pers", "pron-det", "pron-indp", "prp"]

        self.add_arguments_description("tagger", measure.__name__, threeshold, "None")

    def is_user_input_trigger_similar(self, user_input, trigger):
        trigger = filter_non_interrogative_sentence(trigger)

        # tag sentence
        tagged_user_input = self._tagger.tag_sentence(user_input)
        tagged_trigger = self._tagger.tag_sentence(trigger)

        # filtering sentence by the tags
        user_input = self._tagger.construct_sentence(filter_tags(tagged_user_input, self._tags_to_filter_triggers))
        trigger = self._tagger.construct_sentence(filter_tags(tagged_trigger, self._tags_to_filter_triggers))

        # removing stop words and steming
        user_input = RegexUtil.normalize_string(tok_stem(remove_stop_words(user_input)))
        trigger = RegexUtil.normalize_string(tok_stem(remove_stop_words(trigger)))

        return self._measure(user_input, trigger) <= self._threeshold


class Braccard(TriggerSimilarityStrategy):
    def __init__(self, tagger, threshold, weight_tag):
        TriggerSimilarityStrategy.__init__(self)
        self.__tagger = tagger
        self.__threshold = threshold
        self._weight_tag = weight_tag
        self.add_arguments_description("tagger", threshold, weight_tag)

    def is_user_input_trigger_similar(self, user_input, trigger):
        return custom_jaccard(user_input, trigger, self.__tagger, self._weight_tag) >= self.__threshold


class BraccardFilter(TriggerSimilarityStrategy):
    def __init__(self, tagger, threshold, weight_tag):
        TriggerSimilarityStrategy.__init__(self)
        self.__tagger = tagger
        self.__threshold = threshold
        self._weight_tag = weight_tag
        self.add_arguments_description("tagger", threshold)

    def is_user_input_trigger_similar(self, user_input, trigger):
        s1, s2 = remove_stop_words(user_input), remove_stop_words(trigger)
        return custom_jaccard(s1, s2, self.__tagger, self._weight_tag) >= self.__threshold