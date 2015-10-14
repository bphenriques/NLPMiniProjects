# -*- coding: utf-8 -
from TriggersAnswerReader import TriggersAnswerReader
from AnnotationCheck import AnnotationCheck

def sss(fileName, question):

    triggerAnswerReader = TriggersAnswerReader(fileName)
    answer = triggerAnswerReader.get_answer(question)

    if answer is None:
        return "Não sei responder"
    else:
        return answer

def myAvalia(annotationFile, questionsFile):

    #Todo: bad! bad hardcoding, down boy!
    questionsAnswersReader = TriggersAnswerReader("../txt/PerguntasPosSistema.txt")

    annotationCheck = AnnotationCheck(annotationFile)
    answerslist = annotationCheck.your_avalia(annotationFile, questionsAnswersReader, questionsFile)

    return annotationCheck.accuracy(answerslist)