from TriggersAnswerReader import QuestionsAnswerReader
from AnnotationCheck import AnnotationCheck

def sss(fileName, question):

    questionsAnswerReader = QuestionsAnswerReader(fileName)
    answer = questionsAnswerReader.get_answer(question)

    if answer is None:
        return "Não sei responder"
    else:
        return answer

def myAvalia(annotationFile, questionsFile):

    #Todo: bad! bad hardcoding, down boy!
    questionsAnswersReader = QuestionsAnswerReader("../txt/PerguntasPosSistema.txt")

    annotationCheck = AnnotationCheck(annotationFile)
    answerslist = annotationCheck.your_avalia(annotationFile, questionsAnswersReader, questionsFile)

    return annotationCheck.accuracy(answerslist)