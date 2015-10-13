from FileReader import QuestionsAnswerReader
from AnnotatedCheck import your_avalia, accuracy

def sss(fileName, question):

    questionsAnswerReader = QuestionsAnswerReader(fileName)
    return questionsAnswerReader.get_answer(question)

def myAvalia(annotationFile, questionsFile):

    #Todo: bad! bad hardcoding, down boy!
    questionsAnswersReader = QuestionsAnswerReader("../txt/PerguntasPosSistema.txt")

    answerslist = your_avalia(annotationFile, questionsAnswersReader, questionsFile)

    return accuracy(answerslist)