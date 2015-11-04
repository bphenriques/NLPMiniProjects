# -*- coding: utf-8 -*-

from Interface import myAvalia
import Strategies
import sys, traceback

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
        print "================================ RESULTS ==============================="
        print "="
        for strategy in self.__sorted_strategies:
            print "= ", strategy[0].description, ": ", strategy[1]*100, "% accurate"
        print "="
        print "========================================================================"

    def dump_array_strategys(self):
        if len(self.__strategies) == 0:
            print "Empty list of strategies"
            return

        print "========================================================================"
        print "======================= ARRAY OF STRATEGIES ============================"
        print "="

        i = 0
        print "strategies = ["
        for strategy in self.__strategies:
            if strategy[1] == 0.0:
                continue

            print "    create_tuple(Strategies.%s, %s)," %(strategy[0].description, str(strategy[1]))
            i += 1
        print "]"

        print "========================================================================"



def create_tuple(strategy, accuracy=0.0):
    return (strategy, accuracy)



def main():
    annotations_file_path = "TestResources/AnotadoAll.txt"
    questions_file_path = "TestResources/AllCorpusQuestions.txt"
    corpus_file_path = "TestResources/PerguntasPosSistema.txt"

    strategies = []

    # Baseline
    strategies.append(create_tuple(Strategies.IdenticalStrategy(), 0.185345))

    # removing stop words and using stems
    strategies.append(create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswers(), 0.258620689655))


    '''
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(0, 0), 0.258620689655),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(0, 1), 0.258620689655),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(0, 2), 0.26724137931),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(1, 0), 0.258620689655),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(1, 1), 0.258620689655),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(1, 2), 0.26724137931),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(2, 0), 0.26724137931),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(2, 1), 0.26724137931),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(2, 2), 0.275862068966),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(2, 2), 0.275862068966),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(2, 3), 0.275862068966),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(2, 4), 0.275862068966),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(2, 5), 0.275862068966),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(3, 2), 0.301724137931),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(3, 3), 0.301724137931),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(3, 4), 0.301724137931),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(3, 5), 0.301724137931),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(4, 2), 0.379310344828),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(4, 3), 0.379310344828),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(4, 4), 0.375),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(4, 5), 0.375),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(5, 2), 0.400862068966),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(5, 3), 0.405172413793),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(5, 4), 0.400862068966),
        create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(5, 5), 0.400862068966),
    '''

    for i in range(0, 10):
        for j in range(0, 10):
            strategies.append(create_tuple(Strategies.RemoveStopWordsAndStemOnTriggersAndAnswersMED(i, j)))

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
