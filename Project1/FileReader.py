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


def readTrigger(possibleTrigger):
    return re.findall(r"[\s]*T[\s]*-[\s]*[\s\wÀ-ÿ\?!.,-;\"()]+", possibleTrigger)

def readAnswer(possibleAnswer):
    return re.findall(r"[\s]*A[\s]*-[\s]*[\s\wÀ-ÿ\?!.,-;\"()]+", possibleAnswer)


if __name__ == '__main__':
    frasesManhosas = [
        " T - És mesmo parolo!",
        " T - Eu vou à loja do mestra André. É mesmo aqui ao lado!"
        " T - ÀÀÀÀÀAÀÀÀÀÀÀÀ. Derp. Não estou a dizer coisa com coisa (estou?)..."
        " T - E então ele disse: \"Cenas engraçadas",
        " T - E então ele disse: \"Dás me o teu número?"
        " T - Estou preguiçoso. Vou escrever mal. Queres ìr alìh? È que...è que ? Sìgh!",
    ]

    count = 0
    for frase in frasesManhosas:
        result = readTrigger(frase)
        if len(result) > 0:
            count += 1

    print "Got ", count, " correct out of ", len(frasesManhosas)


#readFile("../PerguntasPosSistema.txt")

#print "Cenas -> ", readTrigger(" T - Ena pá! Isto À não é bacÀno? - Diz o Amèdeu. Bem: temos ír que fazer \"isto\"... Atìra o pão ao gato. Cenas (que cenas?); Yap.")