# -*- coding: utf-8 -*-

import re

def readFile(fileName):
    fileIn = open(fileName, 'rU')
    map = getTriggersAndAnswers(fileIn)
    fileIn.close()
    return map

# Stores T and A into a map
def getTriggersAndAnswers(fileIn):

    print "Here..."

    while True:
        # Look for "T - Something?"
        possibleTrigger = fileIn.readline()
        trigger = re.findall(r"[\s]*T[\s]*-[\s]*[\s\wÁ-ÿ\?!.,]+", possibleTrigger)


        print "possibleTrigger: ", possibleTrigger
        print "trigger: ", trigger

        possibleAnswer = fileIn.readline()
        print "possibleAnswer: ", possibleAnswer
        if not possibleAnswer: break  # EOF

        print "I am here bitches"
        answer = re.findall(r"[\s]AT[\s]*-[\s]*[\s\wÁ-ÿ\?!.,]+", possibleTrigger)

        if len(trigger) > 0 and len(answer) > 0:
            print "Trigger: ", trigger
            print "Answer: ", answer
            print "\n"



    return "Hello world"

def readLine(possibleTrigger, trigger):
    rew = RegexWrapper()
    initial_tag = rew.multiple_white_space() + trigger + rew.multiple_white_space() + "-" + rew.multiple_white_space()
    full_regex = initial_tag + rew.at_least_one(rew.diatric_sentence())

    return re.findall(full_regex, possibleTrigger)



class RegexWrapper:
    white_space = "\s"
    utf_letter = "À-ÿ\w"
    letter = "\w"
    diatric = "À-ÿ"
    punctuation = "?!.,-;\"()"

    def diatric_sentence(self):
        return self.re_builder(self.white_space, self.utf_letter, self.punctuation)

    def multiple_white_space(self):
        return self.any(self.re_builder(self.white_space))

    def at_least_one(self, re):
        return re + r"+"

    def any(self, re):
        return re + r"*"

    def optional(self, re):
        return re + r"?"

    def re_builder(self, *chars):
        re_result = r"["
        for char in chars:
            re_result += char

        return re_result + "]"


if __name__ == '__main__':
    frasesManhosas = [
        " T - És mesmo parolo!",
        " T - Eu vou à loja do mestra André. É mesmo aqui ao lado!",
        " T - ÀàÁáÉéèÉÈíÍìÌÓóòÒãõôÔÀÀÀAÀÀÀÀÀÀÀ. Derp. Não estou a dizer coisa com coisa (estou?)...",
        " T - E então ele disse: \"Cenas engraçadas",
        " T - E então ele disse: \"Dás me o teu número?",
        " T - Estou preguiçoso. Vou escrever mal. Queres ìr alìh? È que...è que ? Sìgh!"
    ]

    count = 0
    for frase in frasesManhosas:
        result = readLine(frase, "T")
        print result
        if len(result) > 0:
            count += 1

    print "Got ", count, " correct out of ", len(frasesManhosas)


#readFile("../PerguntasPosSistema.txt")

#print "Cenas -> ", readTrigger(" T - Ena pá! Isto À não é bacÀno? - Diz o Amèdeu. Bem: temos ír que fazer \"isto\"... Atìra o pão ao gato. Cenas (que cenas?); Yap.")