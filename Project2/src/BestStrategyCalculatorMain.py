# -*- coding: utf-8 -*-

import StrategiesForAnswers as sa
import StrategiesForTriggers as st
import sys, traceback
from numpy import arange
from BestStrategyCalculator import BestStrategiesCalculator
from BigramForestTagger import BigramForestTagger


# just keep adding and don't worry
def add_already_calculated(bsc, tagger):
    bsc.add_test(st.IdenticalNormalized(), sa.Identical(), 0.193965517241)
    bsc.add_test(st.RemoveStopWordsAndStem(), sa.RemoveStopWordsAndStem(), 0.254310344828)
    bsc.add_test(st.IdenticalNormalized(), sa.RemoveStopWordsAndStem(), 0.193965517241)
    bsc.add_test(st.RemoveStopWordsAndStem(), sa.Identical(), 0.254310344828)
    bsc.add_test(st.RemoveStopWordsAndStemMED(0), sa.Identical(), 0.254310344828)
    bsc.add_test(st.RemoveStopWordsAndStemMED(0), sa.RemoveStopWordsAndStem(), 0.254310344828)
    bsc.add_test(st.MegaStrategyFiltering(tagger, 0), sa.Identical(), 0.39224137931)
    bsc.add_test(st.MegaStrategyFiltering(tagger, 0), sa.RemoveStopWordsAndStem(), 0.383620689655)
    bsc.add_test(st.RemoveStopWordsAndStemMED(1), sa.Identical(), 0.383620689655)
    bsc.add_test(st.RemoveStopWordsAndStemMED(1), sa.RemoveStopWordsAndStem(), 0.258620689655)


def add_all_combinations(bsc, triggers_strats, answers_strats):
    for trigger_strat in triggers_strats:
        for answer_strat in answers_strats:
            bsc.add_test(trigger_strat, answer_strat)


def get_trigger_strats(tagger):
    result = list()
    result.append(st.IdenticalNormalized())
    result.append(st.RemoveStopWordsAndStem())
    for i in range(0, 5):
        # break
        result.append(st.RemoveStopWordsAndStemMED(i))

    for i in range(0,5):
        break
        result.append(st.MegaStrategyFiltering(tagger, i))

    for i in arange(0, 100, 0.1):
        break
        result.append(st.Braccard(tagger, i))

    for i in arange(0, 100, 0.1):
        break
        result.append(st.MorphoJaccard(tagger, i))

    return result


def get_answer_strats(tagger):
    result = list()
    result.append(sa.Identical())
    result.append(sa.RemoveStopWordsAndStem())
    for i in range(0, 5):
        break
        result.append(sa.RemoveStopWordsAndStemMED(i))

    for i in arange(0, 100, 0.1):
        break
        result.append(sa.Braccard(i))

    return result


def benchmark(annotations_file_path, questions_file_path, corpus_file_path, recalculate=False):
    tagger = BigramForestTagger()  # training corpus floresta
    tagger.train()

    bsc = BestStrategiesCalculator()
    if not recalculate: add_already_calculated(bsc, tagger)  # append already calculated

    #####################################
    # ADD TESTS HERE BELOW
    #####################################

    bsc.add_test(st.IdenticalNormalized(), sa.Identical())

    # two possible ways to test:
    add_all_combinations(bsc, get_trigger_strats(tagger), get_answer_strats(tagger))

    try:
        bsc.determine_best_strategy(annotations_file_path, questions_file_path, corpus_file_path, debug=True)
    except Exception:
        print "\nXXXXXXXXXXXXXXX\nXXXXXXXXXXXXXXX\n"
        traceback.print_exc(file=sys.stdout)
        print "\nXXXXXXXXXXXXXXX\nXXXXXXXXXXXXXXX\n"
    finally:
        print ""
        bsc.dump_array_strategies()
        print ""
        bsc.show_results()


if __name__ == "__main__":
    annotations_file_path = "TestResources/AnotadoAll.txt"
    development_input_file = "TestResources/DevelopmentInput.txt"
    test_input_file = "TestResources/TestInput.txt"

    corpus_file_path = "TestResources/PerguntasPosSistema.txt"

    benchmark(annotations_file_path, development_input_file, corpus_file_path)
    # benchmark(annotations_file_path, test_input_file, corpus_file_path, recalculate=True)