# -*- coding: utf-8 -*-

import StrategiesForAnswers as sa
import StrategiesForTriggers as st
import sys, traceback
import BestStrategyCalculatorPreviousDevel
import BestStrategyCalculatorPreviousTest
from BestStrategyCalculator import BestStrategiesCalculator
from BigramForestTagger import BigramForestTagger
from SimilarityUtil import *

def arange(x, y, jump=0.1):
  while x <= y:
    yield x
    x += jump


def add_all_combinations(bsc, triggers_strats, answers_strats):
    for trigger_strat in triggers_strats:
        for answer_strat in answers_strats:
            bsc.add_test(trigger_strat, answer_strat)

def get_trigger_strats(tagger):
    result = list()
    result.append(st.IdenticalNormalized())

    for filter_value in [False, True]:
        for i in arange(0.25, 0.75, 0.25):
            result.append(st.Jaccard(tagger, i, filter=filter_value))
            result.append(st.Dice(tagger, i, filter=filter_value))

            for j in arange(0.25, 0.75, 0.25):
                result.append(st.Braccard(tagger, i, j, filter=filter_value))

        for i in range(1, 10, 1):
            result.append(st.MED(tagger, i, filter=filter_value))

    return result


def get_answer_strats(tagger):
    result = list()
    result.append(sa.Identical())

    for filter_value in [False, True]:
        for i in arange(0.25, 0.75, 0.25):
            result.append(sa.Jaccard(i, filter=filter_value))
            result.append(sa.Dice(i, filter=filter_value))

            for j in arange(0.25, 0.75, 0.25):
                result.append(sa.Braccard(tagger, i, j, filter=filter_value))

            for weight in arange(0.5, 0.75, 0.25):
                result.append(sa.YesNoSimilar(i, weight, measure=jaccard_sentence, filter=filter_value))
                result.append(sa.YesNoSimilar(i, weight, measure=dice_sentence, filter=filter_value))

        for i in range(1, 10, 1):
            result.append(sa.MED(i, filter=filter_value))

    return result


def benchmark(annotations_file_path, questions_file_path, corpus_file_path, append_previous_func):
    tagger = BigramForestTagger()  # training corpus floresta
    tagger.train()

    bsc = BestStrategiesCalculator()
    append_previous_func(bsc, tagger)

    #####################################
    # ADD TESTS BELOW
    #####################################

    add_all_combinations(bsc, get_trigger_strats(tagger), get_answer_strats(tagger))
    # bsc.add_test(st.Jaccard(tagger, 0.25, False), sa.Braccard(tagger, 0.25, 0.25, False))
    # bsc.add_test(st.Jaccard(tagger, 0.25, False), sa.Braccard(tagger, 0.5, 0.5, True))
    # bsc.add_test(st.Jaccard(tagger, 0.5, False), sa.MED(1, False))
    # bsc.add_test(st.Braccard(tagger, 0.25, 0.25, True), sa.MED(1, False))
    # bsc.add_test(st.Braccard(tagger, 0.25, 0.50, True), sa.YesNoSimilar(0.75, 0.5, dice_sentence, True))
    # bsc.add_test(st.Jaccard(tagger, 0.5, False), sa.YesNoSimilar(0.75, 0.5, dice_sentence, True))
    # bsc.add_test(st.MED(tagger, 2, False), sa.Jaccard(0.5, False))
    # bsc.add_test(st.MED(tagger, 2, False), sa.Dice(0.75, True))

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

    # benchmark(annotations_file_path, development_input_file, corpus_file_path, BestStrategyCalculatorPreviousDevel.add_already_calculated)
    benchmark(annotations_file_path, test_input_file, corpus_file_path, BestStrategyCalculatorPreviousTest.add_already_calculated)