# -*- coding: utf-8 -*-

from Interface import sss, myAvalia
from SimilarityUtil import dice_sentence
from BigramForestTagger import BigramForestTagger
import StrategiesForAnswers as sa
import StrategiesForTriggers as st


if __name__ == "__main__":
    annotations_file_path = "TestResources/AnotadoAll.txt"
    test_input_file = "TestResources/TestInput.txt"
    corpus_file_path = "TestResources/PerguntasPosSistema.txt"

    question_1 = "A tua familia é numerosa?"
    print "Q: ", question_1
    print "R: ", sss(corpus_file_path, question_1)

    print ""

    question_2 = "Tens filhos?"
    print "Q: ", question_1
    print "R: ", sss(corpus_file_path, question_2)

    print ""

    accuracy = myAvalia(annotations_file_path, test_input_file, corpus_file_path)
    print test_input_file, "accuracy is:", accuracy

    ################################
    # Using custom strategies
    ###############################

    tagger = BigramForestTagger()  # training corpus floresta
    tagger.train()

    trigger_strategy = st.Braccard(tagger, 0.25, 0.50, True)
    answer_strategy = sa.YesNoSimilar(0.75, 0.5, dice_sentence, True)

    question_1 = "A tua familia é numerosa?"
    print "Q: ", question_1
    print "R: ", sss(corpus_file_path, question_1, trigger_strategy, answer_strategy)

    print ""

    accuracy = myAvalia(annotations_file_path, test_input_file, corpus_file_path, trigger_strategy, answer_strategy)
    print test_input_file, "accuracy is:", accuracy
