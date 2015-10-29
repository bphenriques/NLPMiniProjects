# -*- coding: utf-8 -*-

from Interface import myAvalia
import Strategies


class BestStrategiesCalculator:

    __strategies = []

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
        for t in self.__strategies:
            if debug: print "Determining accuracy using ", t[0].__class__.__name__, "..."

            if t[1] == 0:
                aux = (t[0], myAvalia(annotation_file, questions_file, corpus_file, strategy=t[0]))
            else:
                aux = (t[0], t[1])

            result.append(aux)

        # sort
        result.sort(key=lambda tup: tup[1], reverse=True)
        self.__strategies = result

    def show_results(self):
        """
        Dump the results sorted by the most accurate strategy to the least accurate
        """
        print "========================================================================"
        print "================================ RESULTS ==============================="
        print "="
        for strategy in self.__strategies:
            print "= ", strategy[0].__class__.__name__, ": ", round(strategy[1], 6)*100, "% accurate"
        print "="
        print "========================================================================"


def create_tuple(strategy, accuracy=0):
    return (strategy, accuracy)

if __name__ == "__main__":
    annotations_file_path = "TestResources/AnotadoAll.txt"
    questions_file_path = "TestResources/AllCorpusQuestions.txt"
    corpus_file_path = "TestResources/PerguntasPosSistema.txt"

    strategies = [
        create_tuple(Strategies.IdenticalStrategy(), 0.185345),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggers(), 0.24569),
        create_tuple(Strategies.RemoveStopWordsAndStemOnAnswers(), 0.25),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswers(), 0.25),
    ]

    bsc = BestStrategiesCalculator(strategies)
    bsc.determine_best_strategy(annotations_file_path, questions_file_path, corpus_file_path, debug=True)
    bsc.show_results()

