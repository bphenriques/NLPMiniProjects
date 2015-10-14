# -*- coding: utf-8 -
from TriggersAnswerReader import TriggersAnswerReader
from AnnotationCheck import AnnotationCheck

def sss(fileName, question):
    trigger_answer_reader = TriggersAnswerReader()
    trigger_answer_reader.process_file(fileName)

    answer = trigger_answer_reader.get_answer(question)

    trigger_answer_reader.dump_map()

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


if __name__ == "__main__":
    print sss("TestResources/PerguntasPosSistema.txt", "Kyle, a minha família é que me salvou.")
