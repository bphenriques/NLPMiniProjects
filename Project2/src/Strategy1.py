from SimilarityStrategy import SimilarityStrategy


class Strategy1(SimilarityStrategy):
    def is_user_input_trigger_similar(self, user_input, trigger):
        return self.normalize_user_input(user_input) == self.normalize_trigger(trigger)

    def are_answer_similar_enough(self, answer1, answer2):
        return answer1 == answer2

