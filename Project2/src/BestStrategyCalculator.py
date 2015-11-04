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

    test_strategy(strategies, Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(0, 0), 0.258620689655)

    for i in range(0, 10):
        for j in range(0, 10):
            pass
            #test_strategy(strategies, Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(i, j))

    # filtering grammatic categories
    for i in range(0, 10):
        for j in range(0, 10):
            pass
            #test_strategy(strategies, Strategies.MegaStrategyFiltering(tagger, i, j))

    # jaccard grammar

    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.0), 0.387931034483)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.05), 0.396551724138)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.1), 0.400862068966)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.15), 0.409482758621)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.2), 0.409482758621)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.25), 0.418103448276)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.3), 0.413793103448)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.35), 0.409482758621)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.4), 0.409482758621)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.45), 0.413793103448)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.5), 0.413793103448)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.55), 0.418103448276)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.6), 0.418103448276)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.65), 0.413793103448)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.7), 0.409482758621)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.75), 0.413793103448)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.8), 0.418103448276)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.85), 0.418103448276)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.9), 0.418103448276)
    test_strategy(strategies, Strategies.MorphoJaccard(tagger, 0.95), 0.418103448276)

    test_strategy(strategies, Strategies.Braccard(tagger, 0.0), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.02), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.04), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.06), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.08), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.1), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.12), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.14), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.16), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.18), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.2), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.22), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.24), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.26), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.28), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.3), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.32), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.34), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.36), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.38), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.4), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.42), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.44), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.46), 0.39224137931)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.48), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.5), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.52), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.54), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.56), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.58), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.6), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.62), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.64), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.66), 0.396551724138)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.68), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.7), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.72), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.74), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.76), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.78), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.8), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.82), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.84), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.86), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.88), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.9), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.92), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.94), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.96), 0.400862068966)
    test_strategy(strategies, Strategies.Braccard(tagger, 0.98), 0.400862068966)

    for i in range(9, 11):
        for j in range(0, 10, 2):
            threshold = float(i)/10 + float(j)/100
            pass
            #test_strategy(strategies, Strategies.MorphoJaccard(tagger, threshold))

    for i in range(0, 10):
        for j in range(0, 10, 2):
            threshold = float(i)/10 + float(j)/100
            test_strategy(strategies, Strategies.Braccard(tagger, threshold))

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
