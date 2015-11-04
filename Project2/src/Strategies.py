# -*- coding: utf-8 -

from SimilarityStrategy import SimilarityStrategy
from SimilarityUtil import *
from RegexUtil import RegexUtil
from BigramForestTagger import BigramForestTagger

# ###########################################
# ###########################################
# ###########################################


class IdenticalStrategy(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2

# ###########################################
# ###########################################
# ###########################################


class RemoveStopWordsAndStemOnTriggers(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = tok_stem(remove_stop_words(self.normalize_user_input(user_input)))
        trigger = tok_stem(remove_stop_words(self.normalize_trigger(trigger)))

        return user_input == trigger

    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2

# ###########################################
# ###########################################
# ###########################################


class RemoveStopWordsAndStemOnAnswers(SimilarityStrategy):

    def is_user_input_trigger_similar(self, user_input, trigger):
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer1)))
        answer2 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer2)))

        return answer1 == answer2

# ###########################################
# ###########################################
# ###########################################


class RemoveStopWordsAndStemOnTriggersAndAnswers(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = tok_stem(remove_stop_words(self.normalize_user_input(user_input)))
        trigger = tok_stem(remove_stop_words(self.normalize_trigger(trigger)))

        return user_input == trigger

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer1)))
        answer2 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer2)))

        return answer1 == answer2

# ###########################################
# ###########################################
# ###########################################


# in short MegaStrategy
class RemoveStopWordsAndStemOnTriggersAndAnswersMED(SimilarityStrategy):
    _med_user_input_triggers_min = 1
    _med_answers_min = 1

    def __init__(self, user_input_triggers_min_med, answers_min_med):
        description = "%s(%s, %s)" %(self.__class__.__name__, str(user_input_triggers_min_med), str(answers_min_med))
        SimilarityStrategy.__init__(self, description)
        self._med_user_input_triggers_min = user_input_triggers_min_med
        self._med_answers_min = answers_min_med

    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = tok_stem(remove_stop_words(self.normalize_user_input(user_input)))
        trigger = tok_stem(remove_stop_words(self.normalize_trigger(trigger)))

        return med(user_input, trigger) <= self._med_user_input_triggers_min

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer1)))
        answer2 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer2)))

        return med(answer1, answer2) <= self._med_answers_min


# ###########################################
# ###########################################
# ###########################################


class MegaStrategyFiltering(SimilarityStrategy):
    _tags_to_filter_triggers = ["n", "in", "prop", "art", "pron-pers", "pron-det", "pron-indp", "prp"]
    _tags_to_filter_answers = []
    _tagger = None

    _med_user_input_triggers_min = 1
    _med_answers_min = 1

    def __init__(self, tagger, user_input_triggers_min_med, answers_min_med, filter_tag_triggers=None, filter_tag_answers=None):
        description = "%s(%s,%s)" %(self.__class__.__name__, str(filter_tag_triggers), str(filter_tag_answers))
        SimilarityStrategy.__init__(self, description)

        self._tagger = tagger
        self._med_user_input_triggers_min = user_input_triggers_min_med
        self._med_answers_min = answers_min_med

        if filter_tag_triggers is not None:
            self._tags_to_filter_triggers = filter_tag_triggers

        if filter_tag_answers is not None:
            self._tags_to_filter_answers = filter_tag_answers

    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = self.normalize_user_input(user_input)
        trigger = self.normalize_trigger(trigger)

        # tag sentence
        tagged_user_input = self._tagger.tag_sentence(user_input)
        tagged_trigger = self._tagger.tag_sentence(trigger)

        # filtering sentence by the tags
        user_input = self._tagger.construct_sentence(filter_tags(tagged_user_input, self._tags_to_filter_triggers))
        tagged_trigger = self._tagger.construct_sentence(filter_tags(tagged_trigger, self._tags_to_filter_triggers))

        # removing stop words and steming
        user_input = tok_stem(remove_stop_words(user_input))
        trigger = tok_stem(remove_stop_words(self.normalize_user_input(trigger)))

        return med(user_input, trigger) <= self._med_user_input_triggers_min

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer1)))
        answer2 = tok_stem(remove_stop_words(RegexUtil.normalize_string(answer2)))

        return med(answer1, answer2) <= self._med_answers_min

