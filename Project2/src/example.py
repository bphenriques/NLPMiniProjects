# -*- coding: utf-8 -*-

from Interface import sss
from Interface import myAvalia

if __name__ == "__main__":
    corpus_src = "TestResources/PerguntasPosSistema.txt"

    question_1 = "A tua familia é numerosa?"
    print "Q: ", question_1
    print "R: ", sss(corpus_src, question_1)

    print ""

    question_2 = "Tens filhos?"
    print "Q: ", question_1
    print "R: ", sss(corpus_src, question_2)

    print ""

    accuracy = myAvalia("TestResources/AnotadoAll.txt", "TestResources/AnnotationsCheckTestsQuestionsSmall.txt", "TestResources/PerguntasPosSistema.txt")
    print "AnnotationsCheckTestsQuestionsSmall.txt accuracy is: ", accuracy
