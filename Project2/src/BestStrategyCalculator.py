# -*- coding: utf-8 -*-

from Interface import myAvalia


class BestStrategiesCalculator:

    __strategies = []
    __sorted_strategies = []

    def __init__(self):
        pass

    def add_test(self, trigger_strategy, answer_strategy, accuracy=0.0):
        tp = self._create_tuple(trigger_strategy, answer_strategy, accuracy)

        if not self._contains_strategy(tp):
            self.__strategies.append(tp)

    def determine_best_strategy(self, annotation_file, questions_file, corpus_file, debug=False):
        """
        For every strategy provided in the constructor, determines the program accuracy and stores the information sorted
        in the variable __strategies

        :param annotation_file: file_path to the annotation file
        :param questions_file: file_path to the questions file
        :param corpus_file: file_path to the corpus file
        :param debug: if true, prints the current strategy being used at a given instance
        :return:
        """
        result = []

        try:
            for tupl in self.__strategies:
                triggers_strat = tupl[0]
                answers_strat = tupl[1]
                accuracy = tupl[2]

                if accuracy == 0.0:
                    if debug: print triggers_strat.description, "# AND #", answers_strat.description, "... ",
                    accuracy = myAvalia(annotation_file, questions_file, corpus_file, trigger_strategy=triggers_strat, answer_strategy=answers_strat)
                    if debug: print str(accuracy*100), "% "

                result.append(self._create_tuple(triggers_strat, answers_strat, accuracy))
        except KeyboardInterrupt:
            print ".... Stopping....."
        finally:
            # sort
            self.__strategies = list(result)
            self.__sorted_strategies = result
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

    def dump_array_strategies(self):
        if len(self.__strategies) == 0:
            print "Empty list of strategies"
            return

        print "========================================================================"
        print "======================= ARRAY OF STRATEGIES ============================"
        print "="

        for strategy in self.__strategies:
            if strategy[1] != 0.0:
                print "bsc.add_test(st.%s, sa.%s, %s" %(strategy[0].description, strategy[1].description, str(strategy[2]) + ")")

        print "="
        print "========================================================================"

    def _contains_strategy(self, strategy):
        for t in self.__strategies:
            if t[0].description == strategy[0].description and t[1].description == strategy[1].description:
                return True
        return False

    def _create_tuple(self, trigger_strategy, answer_strategy, accuracy):
        return (trigger_strategy, answer_strategy, accuracy)

