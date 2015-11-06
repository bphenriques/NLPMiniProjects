# -*- coding: utf-8 -*-

import StrategiesForAnswers as sa
import StrategiesForTriggers as st
import sys, traceback
from BestStrategyCalculatorPrevious import add_already_calculated
from BestStrategyCalculator import BestStrategiesCalculator
from BigramForestTagger import BigramForestTagger


def add_all_combinations(bsc, triggers_strats, answers_strats):
    for trigger_strat in triggers_strats:
        for answer_strat in answers_strats:
            bsc.add_test(trigger_strat, answer_strat)


def get_trigger_strats(tagger):
    result = list()
    result.append(st.IdenticalNormalized())
    result.append(st.RemoveStopWordsAndStem())
    for i in range(0, 10):
        result.append(st.RemoveStopWordsAndStemMED(i))

    for i in range(0, 10):
        result.append(st.MegaStrategyFiltering(tagger, i))

    for i in arange(0, 1, 0.25):
        result.append(st.Braccard(tagger, i))

    for i in arange(0, 1, 0.25):
        result.append(st.MorphoJaccard(tagger, i))

    return result


def get_answer_strats(tagger):
    result = list()
    result.append(sa.Identical())
    result.append(sa.RemoveStopWordsAndStem())
    for i in range(0, 10):
        result.append(sa.RemoveStopWordsAndStemMED(i))

    for i in arange(0, 1, 0.25):
        result.append(sa.Braccard(tagger, i))

    for i in arange(0, 1, 0.25):
        result.append(sa.Jaccard(i))

    for i in arange(0, 1, 0.25):
        result.append(sa.Dice(i))

    for i in arange(0, 1, 0.25):
        result.append(sa.JaccardStem(i))

    for i in arange(0, 1, 0.25):
        result.append(sa.DiceStem(i))

    for i in arange(0, 1, 0.25):
        result.append(sa.YesNoSimilar(i))

    return result

def arange(x, y, jump=0.1):
  while x < y:
    yield x
    x += jump


def benchmark(annotations_file_path, questions_file_path, corpus_file_path, recalculate=False):
    tagger = BigramForestTagger()  # training corpus floresta
    tagger.train()

    bsc = BestStrategiesCalculator()
    if not recalculate: add_already_calculated(bsc, tagger)  # append already calculated

    #####################################
    # ADD TESTS HERE BELOW
    #####################################

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
        bsc.show_results()


if __name__ == "__main__":
    annotations_file_path = "TestResources/AnotadoAll.txt"
    development_input_file = "TestResources/DevelopmentInput.txt"
    test_input_file = "TestResources/TestInput.txt"

    corpus_file_path = "TestResources/PerguntasPosSistema.txt"

    benchmark(annotations_file_path, development_input_file, corpus_file_path)
    # benchmark(annotations_file_path, test_input_file, corpus_file_path, recalculate=True)