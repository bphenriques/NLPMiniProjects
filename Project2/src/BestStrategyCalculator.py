# -*- coding: utf-8 -*-

from Interface import myAvalia
import Strategies
import sys, traceback
from BigramForestTagger import BigramForestTagger


class BestStrategiesCalculator:

    __strategies = []
    __sorted_strategies = []

    def __init__(self, test_strategies):
        """
        Contructor
        :param test_strategies: list of tuples (SimiliaryStrategy, float)  to test
        """

        self.__strategies = test_strategies

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
            for t in self.__strategies:
                if debug: print t[0].description, "..."

                if t[1] == 0:
                    aux = (t[0], myAvalia(annotation_file, questions_file, corpus_file, strategy=t[0]))
                else:
                    aux = (t[0], t[1])

                if debug: print "\t ", str(aux[1]*100), "% "
                result.append(aux)
        except KeyboardInterrupt:
            print ".... Stopping....."
        finally:
            # sort
            self.__strategies = list(result)
            self.__sorted_strategies = result
            self.__sorted_strategies.sort(key=lambda tup: tup[1], reverse=True)

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
            print "= ", strategy[0].description, ": ", strategy[1]*100, "%"
        print "="
        print "========================================================================"

    def dump_array_strategys(self):
        if len(self.__strategies) == 0:
            print "Empty list of strategies"
            return

        print "========================================================================"
        print "======================= ARRAY OF STRATEGIES ============================"
        print "="

        for strategy in self.__strategies:
            if strategy[1] != 0.0:
                print "test_strategy(strategies, Strategies.%s, %s" %(strategy[0].description, str(strategy[1]) + ")")

        print "="
        print "========================================================================"


def test_strategy(strategies, strategy, accuracy=0):
    tp = (strategy, accuracy)
    if not contains_strategy(tp, strategies):
        strategies.append(tp)

def contains_strategy(strategy, tuples_strategies):
    for t in tuples_strategies:
        if t[0].description == strategy[0].description:
            return True
    return False

def main():
    annotations_file_path = "TestResources/AnotadoAll.txt"
    questions_file_path = "TestResources/AllCorpusQuestions.txt"
    corpus_file_path = "TestResources/PerguntasPosSistema.txt"
    strategies = []

    # training corpus floresta
    tagger = BigramForestTagger()
    tagger.train()

    # Baseline
    test_strategy(strategies, Strategies.IdenticalStrategy(), 0.185345)

    # removing stop words and using stems
    test_strategy(strategies, Strategies.RemoveStopWordsAndStemOnTriggersAndAnswers(), 0.258620689655)

    # using med
    for i in range(0, 10):
        for j in range(0, 10):
            pass
            #test_strategy(strategies, Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(i, j))

    # filtering grammatic categories
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 0, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 1, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 2, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 3, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.379310344828)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 4, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 5, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 6, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 7, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 8, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(0, 9, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 0, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 1, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 2, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 3, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 4, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 5, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 6, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 7, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 8, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.387931034483)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(1, 9, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 0, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 1, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 2, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 3, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 4, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 5, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 6, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 7, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 8, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(2, 9, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 0, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 1, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 2, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 3, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 4, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.39224137931)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 5, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 6, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 7, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.396551724138)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 8, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.400862068966)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(3, 9, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.400862068966)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 0, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.405172413793)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 1, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.405172413793)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 2, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.405172413793)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 3, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.405172413793)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 4, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.400862068966)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 5, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.400862068966)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 6, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.400862068966)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 7, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.405172413793)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 8, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.405172413793)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(4, 9, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.405172413793)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(5, 0, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.409482758621)
    test_strategy(strategies, Strategies.MegaStrategyFiltering(5, 1, ['n', 'in', 'prop', 'art', 'pron-pers', 'pron-det', 'pron-indp', 'prp'], []), 0.409482758621)

    for i in range(0, 10):
        for j in range(0, 10):
            test_strategy(strategies, Strategies.MegaStrategyFiltering(tagger, i, j))

    bsc = BestStrategiesCalculator(strategies)
    try:
        bsc.determine_best_strategy(annotations_file_path, questions_file_path, corpus_file_path, debug=True)
    except Exception:
        print "\nXXXXXXXXXXXXXXX\nXXXXXXXXXXXXXXX\n"
        traceback.print_exc(file=sys.stdout)
        print "\nXXXXXXXXXXXXXXX\nXXXXXXXXXXXXXXX\n"
    finally:
        bsc.show_results()
        bsc.dump_array_strategys()

if __name__ == "__main__":
    main()
