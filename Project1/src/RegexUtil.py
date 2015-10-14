# -*- coding: utf-8 -*-

import re

class RegexUtil:
    white_space = "\s"
    utf_letter = "À-ÿ\w"
    letter = "\w"
    diatric = "À-ÿ"
    punctuation = "?!.,-;\"()"
    anything = "."

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


    def normalize_string(self, sentence):
        sentence = sentence.lower()
        sentence = self.remove_diacritics(sentence)
        sentence = self.remove_punctuation(sentence)
        return sentence

    def remove_punctuation(self, sentence):
        sentence = re.sub("[:;,\.\?!]", '', sentence)
        sentence = re.sub("[\"\(\)]", '', sentence)
        sentence = re.sub("[\r\n]", '', sentence)
        return sentence

    def remove_diacritics(self, sentence):
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
