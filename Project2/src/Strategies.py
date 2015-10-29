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
        user_input = tok_stem(remove_words(self.normalize_user_input(user_input)))
        trigger = tok_stem(remove_words(self.normalize_user_input(trigger)))

        return user_input == trigger

    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2

class RemoveStopWordsAndStemOnAnswers(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_words(self.normalize_user_input(answer1)))
        answer2 = tok_stem(remove_words(self.normalize_user_input(answer2)))

        return answer1 == answer2

class RemoveStopWordsAndStemOnTriggersAndAnswers(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        user_input = tok_stem(remove_words(self.normalize_user_input(user_input)))
        trigger = tok_stem(remove_words(self.normalize_user_input(trigger)))

        return user_input == trigger

    def are_answer_similar_enough(self, answer1, answer2):
        answer1 = tok_stem(remove_words(self.normalize_user_input(answer1)))
        answer2 = tok_stem(remove_words(self.normalize_user_input(answer2)))

        return answer1 == answer2

