# -*- coding: utf-8 -*-
import re

# Lowercases a string and removes diacritics and punctuation from a portuguese sentence
#
def normalizestring(sentence):

    sentence = sentence.lower()
    sentence = removediacritics(sentence)
    sentence = re.sub("[:;,\.\?!]", "", sentence)
    return sentence


def removediacritics(sentence):
    # a
    sentence = sentence.replace('á', 'a')
    sentence = sentence.replace('à', 'a')
    sentence = sentence.replace('ã', 'a')
    sentence = sentence.replace('â', 'a')
    # e
    sentence = sentence.replace('é', 'e')
    sentence = sentence.replace('è', 'e')
    sentence = sentence.replace('ẽ', 'e')
    sentence = sentence.replace('ê', 'e')
    # i
    sentence = sentence.replace('í', 'i')
    sentence = sentence.replace('ì', 'i')
    sentence = sentence.replace('ĩ', 'i')
    sentence = sentence.replace('î', 'i')
    # o
    sentence = sentence.replace('ó', 'o')
    sentence = sentence.replace('ò', 'o')
    sentence = sentence.replace('ô', 'o')
    sentence = sentence.replace('õ', 'o')
    # u
    sentence = sentence.replace('ú', 'u')
    sentence = sentence.replace('ù', 'u')
    sentence = sentence.replace('ũ', 'u')
    sentence = sentence.replace('û', 'u')
    # c
    sentence = sentence.replace('ç', 'c')
    return sentence

banana = "atiréi o páu ao çaçto, MAS o tróll não morrêu!"

print normalizestring(banana)