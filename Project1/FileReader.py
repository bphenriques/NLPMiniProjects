# -*- coding: utf-8 -*-

import os

def readFile(fileName):
    #fileIn = open(fileName, 'rU')
    #profset = getTriggersAndAnswers(fileIn)
    #fileIn.close()

# Stores T and A into a map
def profNER(file):
    numLinha = 0
    myset = []
    for line in file:
        numLinha = numLinha + 1
        results = re.findall(r"[^-?\.:.]\s[A-Z][\w]+[\s\?]", line)
        i = 0
        print(results)
        while i < len(results):
            nomePessoa = re.search(r"([A-Z][\w]+)", results[i])
            m = str(numLinha), nomePessoa.group(1)
            i = i + 1
            myset.append(m)
    print_list(myset)
    return set(myset)