from RegexUtil import RegexUtil

class SimilarityStrategy:

    #verify using word/sentence distance if a trigger is close enough
    def is_similar_enough(self, user_input, trigger):
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2

    def normalize_user_input(self, user_input):
        # lowercase, no punctuation diacritics transformation
        return RegexUtil.normalize_string(user_input)

    def normalize_trigger(self, trigger):
        # lowercase, no punctuation diacritics transformation
        return RegexUtil.normalize_string(trigger)

    def normalize_answer(self, answer):
        return answer

    def is_user_input_trigger_identical(self, user_input, trigger):
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

