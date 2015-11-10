# -*- coding: utf-8 -

from RegexUtil import RegexUtil
from SimilarityStrategies import TriggerSimilarityStrategy
from SimilarityUtil import *


class IdenticalNormalized(TriggerSimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return RegexUtil.normalize_string(user_input) == RegexUtil.normalize_string(trigger)


# Applys extra filter on gramatical category
class MegaStrategyFiltering(TriggerSimilarityStrategy):
    def __init__(self, tagger, filter_tag_triggers=None):
        TriggerSimilarityStrategy.__init__(self)
        self._tagger = tagger
        if filter_tag_triggers is not None:
            self._tags_to_filter_triggers = filter_tag_triggers
        else:
            self._tags_to_filter_triggers = ["n", "in", "prop", "art", "pron-pers", "pron-det", "pron-indp", "prp"]

    def filter_sentence(self, sentence):
        sentence = filter_non_interrogative_sentence(sentence)
        tagged_sentence = self._tagger.tag_sentence(sentence)

        # filtering sentence by the tags
        sentence = self._tagger.construct_sentence(filter_tags(tagged_sentence, self._tags_to_filter_triggers))

        # removing stop words and steming
        sentence = RegexUtil.normalize_string(tok_stem(remove_stop_words(sentence)))
        return sentence

    def is_user_input_trigger_similar(self, user_input, trigger):
        pass


class Jaccard(MegaStrategyFiltering):
    def __init__(self, tagger, threeshold, filter, filter_tag_triggers=None):
        MegaStrategyFiltering.__init__(self, tagger, filter_tag_triggers)
        self._threeshold = threeshold
        self._filter = filter
        self.add_arguments_description("tagger", threeshold, filter, "None")

    def is_user_input_trigger_similar(self, user_input, trigger):
        if self._filter:
            user_input, trigger = self.filter_sentence(user_input), self.filter_sentence(trigger)
        else:
            user_input, trigger = RegexUtil.normalize_string(user_input),  RegexUtil.normalize_string(trigger)

        return jaccard_sentence(self.filter_sentence(user_input), self.filter_sentence(trigger)) >= self._threeshold


class Dice(MegaStrategyFiltering):
    def __init__(self, tagger, threeshold, filter, filter_tag_triggers=None):
        MegaStrategyFiltering.__init__(self, tagger, filter_tag_triggers)
        self._threeshold = threeshold
        self._filter = filter
        self.add_arguments_description("tagger", threeshold, filter, "None")

    def is_user_input_trigger_similar(self, user_input, trigger):
        if self._filter:
            user_input, trigger = self.filter_sentence(user_input), self.filter_sentence(trigger)
        else:
            user_input, trigger = RegexUtil.normalize_string(user_input),  RegexUtil.normalize_string(trigger)

        return dice_sentence(user_input, trigger) >= self._threeshold


class MED(MegaStrategyFiltering):
    def __init__(self, tagger, threeshold, filter, filter_tag_triggers=None):
        MegaStrategyFiltering.__init__(self, tagger, filter_tag_triggers)
        self._threeshold = threeshold
        self._filter = filter
        self.add_arguments_description("tagger", threeshold, filter, "None")

    def is_user_input_trigger_similar(self, user_input, trigger):
        if self._filter:
            user_input, trigger = self.filter_sentence(user_input), self.filter_sentence(trigger)
        else:
            user_input, trigger = RegexUtil.normalize_string(user_input),  RegexUtil.normalize_string(trigger)

        return med_sentence(user_input, trigger) <= self._threeshold


class Braccard(TriggerSimilarityStrategy):
    def __init__(self, tagger, threshold, weight_tag, filter):
        TriggerSimilarityStrategy.__init__(self)
        self.__tagger = tagger
        self.__threshold = threshold
        self._weight_tag = weight_tag
        self._filter = filter
        self.add_arguments_description("tagger", threshold, weight_tag, filter)

    def is_user_input_trigger_similar(self, user_input, trigger):
        if self._filter:
            user_input, trigger = remove_stop_words(user_input), remove_stop_words(trigger)

        return custom_jaccard(user_input, trigger, self.__tagger, self._weight_tag) >= self.__threshold