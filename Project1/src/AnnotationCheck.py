# -*- coding: utf-8 -
import re
from RegexUtil import RegexUtil

from TriggersAnswerReader import TriggersAnswerReader

class AnnotationCheck:

    _annotationFilePath = ''

    def __init__(self, annotationFilePath):
        self._annotationFilePath = annotationFilePath

    def your_avalia(self, annotationFile, questionsAnswersReader, questionsFilePath):

        answerslist = list()
        with open(questionsFilePath) as questionFile:
            for line in questionFile:
                answer = questionsAnswersReader.get_answer(line)
                # Todo: not opening the file on every iteration
                annotation = self.get_annotation(line, answer, 20)
                answerslist.append(annotation)
            questionFile.close()

        return answerslist


    def get_annotation(self, question, answer, nanswers):

        rxutil = RegexUtil()
        #Todo verificar filepath e nanswers
        file = open(self._annotationFilePath)
        normalizedquestion = rxutil.normalize_string(question)

        line = file.readline()
        while (line):
            normalizedline = rxutil.normalize_string(line)
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


    def accuracy(self, answers):

        tp = 0
        for x in answers:
            if(x == 'y'):
                tp = tp + 1

        return float(tp) / len(answers)
#banana = list("ynmym")
#banana = ['y', 'n', 'm']
#print accuracy(banana)
#ac = AnnotationCheck("txt/AnotadoAll.txt")
#print ac.get_annotation("És aluno do Técnico?", "Isso é a coisa mais burra que disse desde há algum tempo.", 20)