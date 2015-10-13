# -*- coding: utf-8 -
import re
from Normalizer import normalizestring

def myAvalia(annotationFile, questionsFile):

    return accuracy(list())


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
    fp = 0
    tn = 0
    fn = 0

    for x in answers:
        if(x == 'y'):
            tp = tp + 1
        elif (x == 'n' | x== 'm'):
            fp = fp +1
    return 1 #accuracy perfeita ó


#print getannotation("És aluno do Técnico?", "Isso é a coisa mais burra que disse desde há algum tempo.", "../AnotadoAll.txt", 20)