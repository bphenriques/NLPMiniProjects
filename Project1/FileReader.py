# -*- coding: utf-8 -*-

import re
from RegexWrapper import RegexWrapper

class QuestionsAnswerReader:
    __TRIGGER_TAG = "T"
    __ANSWER_TAG = "A"

    fileName = ""
    __trigger_regex = ""
    __answer_regex = ""

    def __init__(self, fileName):
        self.fileName = fileName

        rew = RegexWrapper()
        self.trigger_tag = rew.multiple_white_space() + self.__TRIGGER_TAG + rew.multiple_white_space() + "-" + rew.multiple_white_space()
        self.answer_tag = rew.multiple_white_space() + self.__ANSWER_TAG + rew.multiple_white_space() + "-" + rew.multiple_white_space()
        self.__trigger_regex = self.trigger_tag + rew.at_least_one(rew.diatric_sentence())
        self.__answer_regex = self.answer_tag + rew.at_least_one(rew.diatric_sentence())

    def processFile(self):
        fileIn = open(self.fileName, 'rU')
        self._getTriggersAndAnswers(fileIn)
        fileIn.close()
        return map

    # Stores T and A into a map
    def _getTriggersAndAnswers(self, fileIn):
        while True:
            # Look for "T - Something?"
            trigger = self._readLine(fileIn.readline(), self.__trigger_regex)
            if len(trigger) < 0:
                break

            possibleAnswer = fileIn.readline()
            if not possibleAnswer: break  # EOF
            answer = self._readLine(possibleAnswer, self.__answer_regex)
            if len(answer) < 0:
                break

            if __debug__:
                if len(trigger) > 0:
                    print "Trigger: ", trigger
                if len(answer) > 0:
                    print "Answer: ", answer

    def _readLine(self, possibleTrigger, regex):
        return re.findall(regex, possibleTrigger)


#For testing
class TestQuestionsAnswerReader(QuestionsAnswerReader):
    def testTriggerReader(self, possibleTrigger):
        return self.__readLine(possibleTrigger, self.__trigger_regex)

    def testAnswerReader(self, possibleAnswer):
        return self.__readLine(possibleAnswer, self.__answer_regex)



def testTriggerRegex():
    frasesManhosas = [
        " T - És mesmo parolo!",
        " T - Eu vou à loja do mestra André. É mesmo aqui ao lado!",
        " T - ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ. Derp. Não estou a dizer coisa com coisa (estou?)...",
        " T - E então ele disse: \"Cenas engraçadas",
        " T - E então ele disse: \"Dás me o teu número?",
        " T - Estou preguiçoso. Vou escrever mal. Queres ìr alìh? È que...è que ? Sìgh!"
    ]

    qar = QuestionsAnswerReader("")

    count = 0
    for frase in frasesManhosas:
        result = qar.testTriggerReader(frase)
        print result
        if len(result) > 0:
            count += 1

    print "Got ", count, " correct out of ", len(frasesManhosas)

def testReadFile(fileName):
    questions_answer_reader = TestQuestionsAnswerReader(fileName)
    questions_answer_reader.processFile()
    print "Done"


if __name__ == '__main__':
    testReadFile("../PerguntasPosSistema.txt")
    #testTriggerRegex()