# -*- coding: utf-8 -

from RegexUtil import RegexUtil
from SimilarityStrategies import TriggerSimilarityStrategy
from SimilarityUtil import *

# ###########################################
# ###########################################
# ###########################################


class IdenticalNormalized(TriggerSimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return RegexUtil.normalize_string(user_input) == RegexUtil.normalize_string(filter_non_interrogative_sentence(trigger))

# ###########################################
# ###########################################
# ###########################################


class RemoveStopWordsAndStem(TriggerSimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = RegexUtil.normalize_string(tok_stem(remove_stop_words(user_input)))
        trigger = RegexUtil.normalize_string(filter_non_interrogative_sentence(tok_stem(remove_stop_words(trigger))))

        return user_input == trigger


# ###########################################
# ###########################################
# ###########################################


class RemoveStopWordsAndStemMED(TriggerSimilarityStrategy):
    def __init__(self, user_input_triggers_min_med):
        TriggerSimilarityStrategy.__init__(self)

        self.add_arguments_description(user_input_triggers_min_med)
        self._med_user_input_triggers_min = user_input_triggers_min_med

    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = RegexUtil.normalize_string(tok_stem(remove_stop_words(user_input)))
        trigger = RegexUtil.normalize_string(filter_non_interrogative_sentence(tok_stem(remove_stop_words(trigger))))

        return med(user_input, trigger) <= self._med_user_input_triggers_min


# ###########################################
# ###########################################
# ###########################################


class MegaStrategyFiltering(TriggerSimilarityStrategy):
    def __init__(self, tagger, user_input_triggers_min_med, filter_tag_triggers=None):
        TriggerSimilarityStrategy.__init__(self)

        self._tagger = tagger
        self._med_user_input_triggers_min = user_input_triggers_min_med

        if filter_tag_triggers is not None:
            self._tags_to_filter_triggers = filter_tag_triggers
        else:
            self._tags_to_filter_triggers = ["n", "in", "prop", "art", "pron-pers", "pron-det", "pron-indp", "prp"]

        self.add_arguments_description("tagger", user_input_triggers_min_med, self._tags_to_filter_triggers)

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

        return med(user_input, trigger) <= self._med_user_input_triggers_min

# ###########################################
# ###########################################
# ###########################################


class MorphoJaccard(TriggerSimilarityStrategy):
    def __init__(self, tagger, threshold = 0.8):
        TriggerSimilarityStrategy.__init__(self)
        self.__tagger = tagger
        self.__threshold = threshold
        self.add_arguments_description("tagger", threshold)

    def is_user_input_trigger_similar(self, user_input, trigger):
        s1 = RegexUtil.normalize_string(user_input)
        s2 = RegexUtil.normalize_string(filter_non_interrogative_sentence(trigger))
        return custom_jaccard(s1, s2, self.__tagger) >= self.__threshold


class Braccard(TriggerSimilarityStrategy):
    def __init__(self, tagger, threshold = 0.8):
        TriggerSimilarityStrategy.__init__(self)
        self.__tagger = tagger
        self.__threshold = threshold
        self.add_arguments_description("tagger", threshold)

    def is_user_input_trigger_similar(self, user_input, trigger):
        s1 = RegexUtil.normalize_string(user_input)
        s2 = RegexUtil.normalize_string(filter_non_interrogative_sentence(trigger))
        return custom_jaccard(s1, s2, self.__tagger) >= self.__threshold
