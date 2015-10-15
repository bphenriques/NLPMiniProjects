# -*- coding: utf-8 -
import re
import os.path
from RegexUtil import RegexUtil

from TriggersAnswerReader import TriggersAnswerReader

class AnnotationCheck:

    _annotationFilePath = ''
    __rxutil = RegexUtil()

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


    def get_annotation(self, user_input, answer, max_n_answers):
        """
        Gets the corresponding annotation from the answer given an user-input

        To simplify and since it wasn't required, the user_input is not normalized,
        i.e., keep case, keep diacritric and keep ponctuation

        :param user_input:
        :param answer:
        :param max_n_answers:
        :return: the annotation
        """

        #Todo: Possible upgrade, verificar filepath e nanswers
        file_in = open(self._annotationFilePath)
        match_question_regex = "User Input[\s]*-[\s]*" + user_input

        line = file_in.readline()
        while line:
            match_question = re.search(match_question_regex, line)
            if match_question is not None:
                for i in range(0, max_n_answers):
                    answer_line = file_in.readline()

                    # find specific answer
                    match_answer = re.search(answer + "[\s]*:[\s]*[ymn]", answer_line)
                    if match_answer is not None:
                        #clean up found
                        annotation_regex = "[\s]*A[\s]*-[\s]*" + answer + "[\s]*:[\s]*"
                        annotation = re.sub(annotation_regex, '', match_answer.string)
                        annotation = re.sub("\n", '', annotation)
                        file_in.close()
                        return annotation
            line = file_in.readline()


    def accuracy(self, answers, positive_char = 'y'):
        if len(answers) == 0: return 0

        tp = answers.count(positive_char)
        return float(tp) / len(answers)

#banana = list("ynmym")
#banana = ['y', 'n', 'm']
#print accuracy(banana)
#ac = AnnotationCheck("txt/AnotadoAll.txt")
#print ac.get_annotation("És aluno do Técnico?", "Isso é a coisa mais burra que disse desde há algum tempo.", 20)