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
        trigger = re.findall(r"[\s]*T[\s]*-[\s]*[\s\wÁ-ÿ]+[?\!.,]*", possibleTrigger)
        print "possibleAnswer: ", possibleTrigger
        print "trigger: ", trigger

        possibleAnswer = fileIn.readline()
        print "possibleAnswer: ", possibleAnswer
        if not possibleAnswer: break  # EOF

        print "I am here bitches"
        answer = re.findall(r"[\s]*A[\s]*-[\s]*[\w\s]+[?\!.,]*", possibleTrigger)

        if len(trigger) > 0 and len(answer) > 0:
            print "Trigger: ", trigger
            print "Answer: ", answer
            print "\n"



    return "Hello world"


def PortugueseSentenceRE():
    return ""

readFile("../PerguntasPosSistema.txt")
