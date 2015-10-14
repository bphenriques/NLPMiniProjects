# -*- coding: utf-8 -
from TriggersAnswerReader import TriggersAnswerReader
from AnnotationCheck import AnnotationCheck

def sss(fileName, question):
    trigger_answer_reader = TriggersAnswerReader()
    trigger_answer_reader.process_file(fileName)
    #trigger_answer_reader.dump_map()
    answer = trigger_answer_reader.get_answer(question)
    if answer is None:
        answer = "Não sei responder"
    return answer.decode("utf-8")

def myAvalia(annotationFile, questionsFile):

    #Todo: bad! bad hardcoding, down boy!
    questionsAnswersReader = TriggersAnswerReader()
    questionsAnswersReader.process_file("TestResources/PerguntasPosSistema.txt")

    annotationCheck = AnnotationCheck(annotationFile)
    answerslist = annotationCheck.your_avalia(annotationFile, questionsAnswersReader, questionsFile, 20)

    return annotationCheck.accuracy(answerslist)


if __name__ == "__main__":

    # The following question has no triggers that are similar to the user input
    assert sss("TestResources/PerguntasPosSistema.txt", "A tua familia é numerosa?") == u"Não sei responder"

    #Non existent at all
    assert sss("TestResources/PerguntasPosSistema.txt", "I DONT EXIST?") == u"Não sei responder"

    #There are many similar triggers with this user_input
    assert sss("TestResources/PerguntasPosSistema.txt", "Tens filhos?") == u"Não."

    print "Passed sss tests"
