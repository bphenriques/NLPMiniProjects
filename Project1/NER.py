# -*- coding: utf-8 -*-
import os, re, codecs
from nltk.metrics.scores import precision, recall

wordsToFilter = [
    "Queres",
    "Lisboa",
    "Gosto",
    "Do",
    "Tenho",
    "Sim",
    "Eu"
    "Porque",
    "Vou",
    "Não",
    "Quem",
    "Que",
    "Por",
    "Ie",
    "De",
    "Planeei",
    "Sei",
    "Adorava",
    "Vou",
    "Olha",
    "Pai",
    "Dame",
    "Da",
    "Ela",
    "Desde",
    "Queres",
    "Chefe",
    "Eu",
    "Obrigado",
    "Certo",
    "Gostas",
    "Como",
    "Cheve",
    "Este",
    "Acho",
    "Americanos",
    "Ah",
    "Talvez",
    "Provavelmente",
    "Hummmmm",
    "Vozes",
    "Do",
    "Ainda",
    "Eles",
    "Porque",
    "Nadar",
    "espIendor"
    "Estes",
    "Canal",
    "Isso",
    "Desculpa",
    "Eis",
    "Argentina",
    "Bem",
    "Resulta",
    "Preciso",
    "Vamos",
    "Pensas",
    "Confia",
    "Exato",
    "Ora",
    "Claro",
    "Podes",
    "Compro",
    "Temos",
    "Pois",
    "Onde",
    "Nada",
    "Estou",
    "Era",
    "Podemos",
    "Se",
    "Fazer",
    "Podermos",
    "Solta",
]

#https://docs.python.org/2/library/re.html

# --------------
# python
# import nltk
# from NER import profNER
# --------------

# -----------------------------------------
# Formato do ficheiro de entrada
# T - Queres ir dar uma volta por Lisboa?
# 	A - O que é que estás a fazer? : n

# Compara com ref
# Precision e recall
# -----------------------------------------

# --------------
# Procura EM, nomes de pessoas, bem como a linha onde se encontram.
# Devolve set na forma
# ('numLinha', 'nomePessoa)
# --------------

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


def myNER(file):
    numLinha = 0
    myset = []
    for line in file:
        numLinha = numLinha + 1
        results = re.findall(r"[\w,\.\?!]*[\s]*[A-Z][\w]+[\s\?\.,!]", line) #\s = spaco branco, \w = [a-zA-Z0-9]

        if len(results) != 0:
            print numLinha, ": ", results
            i = 0
            while i < len(results):
                aux = re.split(r"[\W\s]", results[i]) # Split by whitespace or punctuation
                print "aux: ", aux
                j = 0
                while j < len(aux):
                    component = aux[j].strip()
                    if component not in wordsToFilter:
                        nomePessoa = re.search(r"([A-Z][\w]+)", component)
                        if nomePessoa:
                            print "--->", nomePessoa.group(1)
                            m = str(numLinha), nomePessoa.group(1)
                            myset.append(m)
                    j = j + 1
                i = i + 1
    print_list(myset)
    return set(myset)

# ---------------
# Faz o print de uma lista
# ---------------
def print_list(list):
    j = 0
    while j < len(list):
        print list[j]
        j = j + 1


# ---------------
# Lê a ref
# ----------------
def read_ref(file):
    ref = []
    for line in file:
        numLinha = re.search(r"(\d+)", line)
        nomePessoa = re.search(r"([A-Z][\w]+)", line)
        m = numLinha.group(1), nomePessoa.group(1)
        ref.append(m)
    #print_list(ref)
    return set(ref)

# --------------
# Extrai NE
# --------------
fileIn = open('Corpora/dev.txt', 'rU')
profset = myNER(fileIn)
fileIn.close()

# --------------
# Extrai REF
# --------------

fileRef = open('Corpora/dev-ref.txt', 'rU')
ref = read_ref(fileRef)
fileRef.close()

# --------------
# Calcula precision e recall
# --------------

print "Precision Baseline:", precision(profset, ref)
print "Recall Baseline:", recall(profset, ref)