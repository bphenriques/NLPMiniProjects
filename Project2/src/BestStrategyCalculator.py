# -*- coding: utf-8 -*-

from Interface import myAvalia


class BestStrategiesCalculator:
    """
    Test class for different combinations of AnswerSimilarityStrategy and TriggerSimilarityStrategy
    """

    def __init__(self):
        self.__strategies = list()
        self.__strategies_map = {}
        self.__sorted_strategies = list()

    def add_test(self, trigger_strategy, answer_strategy, accuracy=None):
        """

        :param trigger_strategy: Strategy for comparing user input and trigger
        :param answer_strategy: Strategy for comparing two answers
        :param accuracy: Default is None. Put value different than None to skip and use the value provided.
        """
        tp = self._create_tuple(trigger_strategy, answer_strategy, accuracy)

        key = self.__key(trigger_strategy, answer_strategy)
        if key not in self.__strategies_map:
            self.__strategies_map[key] = True # place holder
            self.__strategies.append(tp)

    def __key(self, trigger_strat, answer_strat):
        return trigger_strat.description + "-" + answer_strat.description

    def determine_best_strategy(self, annotation_file, questions_file, corpus_file, debug=False):
        """
        For every strategy provided in the constructor, determines the program accuracy and stores the information sorted
        in the variable __strategies_map

        :param annotation_file: file_path to the annotation file
        :param questions_file: file_path to the questions file
        :param corpus_file: file_path to the corpus file
        :param debug: if true, prints the current strategy being used at a given instance
        """
        result = []

        try:
            for tupl in self.__strategies:
                triggers_strat = tupl[0]
                answers_strat = tupl[1]
                accuracy = tupl[2]

                if accuracy is None:
                    if debug: print "bsc.add_test(st." + triggers_strat.description + ", sa." + answers_strat.description + ", ",
                    accuracy = myAvalia(annotation_file, questions_file, corpus_file, trigger_strategy=triggers_strat, answer_strategy=answers_strat)
                    if debug: print str(accuracy) + ")"

                result.append(self._create_tuple(triggers_strat, answers_strat, accuracy))

        except KeyboardInterrupt:
            print ".... Stopping....."
        finally:
            # sort
            self.__strategies = list(result)
            self.__sorted_strategies = list(result)
            self.__sorted_strategies.sort(key=lambda tup: tup[2], reverse=True)

    def show_results(self):
        """
        Dump the results sorted by the most accurate strategy to the least accurate
        """

        if len(self.__sorted_strategies) == 0:
            print "Empty list of strategies"
            return

        print "========================================================================"
        print "======================== ACCURACY RESULTS =============================="
        print "="
        for strategy in self.__sorted_strategies:
            print "= TRIGGER", strategy[0].description, " ", str(strategy[2]*100), "% "
            print "= ANSWER ", strategy[1].description
            print "= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
        print "="
        print "========================================================================"

    def _create_tuple(self, trigger_strategy, answer_strategy, accuracy):
        return (trigger_strategy, answer_strategy, accuracy)

