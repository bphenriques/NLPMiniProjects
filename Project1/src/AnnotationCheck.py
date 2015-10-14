# -*- coding: utf-8 -
import re
import os.path
from RegexUtil import RegexUtil

from TriggersAnswerReader import TriggersAnswerReader

class AnnotationCheck:

    _annotationFilePath = ''

    def __init__(self, annotationFilePath):
        if not os.path.exists(annotationFilePath):
            print "File not found"
            raise Exception
        self._annotationFilePath = annotationFilePath


    def your_avalia(self, questionsAnswersReader, questionsFilePath, maxnanswers):

        answerslist = list()
        with open(questionsFilePath) as questionFile:
            for line in questionFile:
                answer = questionsAnswersReader.get_answer(line)

                if answer is not None:
                    annotation = self.get_annotation(line, answer, maxnanswers)
                    if annotation is None:
                        annotation = 'n'
                else:
                    annotation = 'n'
                answerslist.append(annotation)
            questionFile.close()
        return answerslist


    def get_annotation(self, question, answer, max_n_answers):

        rxutil = RegexUtil()
        #Todo: Possible upgrade, verificar filepath e nanswers
        file = open(self._annotationFilePath)
        normalizedquestion = rxutil.normalize_string(question)
        line = file.readline()
        while (line):
            normalizedline = rxutil.normalize_string(line)
            matchquestion = re.search("user input - " + normalizedquestion, normalizedline)
            if (matchquestion is not None):
                for i in range(0, max_n_answers):
                    answerline = file.readline()
                    matchanswer = re.search(answer + " : [ymn]", answerline)
                    if (matchanswer is not None):
                        annotation = re.sub("[\s]*A - " + answer + " : ", '', matchanswer.string)
                        annotation = re.sub("\n", '', annotation)
                        file.close()
                        return annotation
            line = file.readline()


    def accuracy(self, answers):
        tp = answers.count('y')
        return float(tp) / len(answers)
#banana = list("ynmym")
#banana = ['y', 'n', 'm']
#print accuracy(banana)
#ac = AnnotationCheck("txt/AnotadoAll.txt")
#print ac.get_annotation("És aluno do Técnico?", "Isso é a coisa mais burra que disse desde há algum tempo.", 20)