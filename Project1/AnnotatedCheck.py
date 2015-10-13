# -*- coding: utf-8 -
import re
from Normalizer import normalizestring

def myAvalia(annotationFile, questionsFile):

    answerslist = list()

    open(questionsFile)
    with open(questionsFile) as file:
        for line in file:
            question = line
            answer = get_answer(line)
            #Todo: not opening the file on every iteration
            annotation = getannotation(line, answer, annotationFile, 20)
            answerslist.append(annotation)

    return accuracy(answerslist)


def getannotation(question, answer, filepath, nanswers):
    #Todo verificar filepath e nanswers
    file = open(filepath)
    normalizedquestion = normalizestring(question)

    line = file.readline()
    while (line):
        normalizedline = normalizestring(line)
        matchquestion = re.search("user input - " + normalizedquestion, normalizedline)
        if (matchquestion is not None):
            for i in range(0, nanswers):
                answerline = file.readline()
                matchanswer = re.search(answer + " : [ymn]", answerline)
                if (matchanswer is not None):
                    annotation = re.sub("[\s]*A - " + answer + " : ", '', matchanswer.string)
                    file.close()
                    return annotation
        line = file.readline()


def accuracy(answers):
    tp = 0


    for x in answers:
        if(x == 'y'):
            tp = tp + 1

    return float(tp) / len(answers) #accuracy perfeita ó
#ibanana = list("ynmym")
#banana = ['y', 'n', 'm']
print accuracy(banana)
#print getannotation("És aluno do Técnico?", "Isso é a coisa mais burra que disse desde há algum tempo.", "../AnotadoAll.txt", 20)