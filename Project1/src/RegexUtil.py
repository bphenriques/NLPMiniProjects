# -*- coding: utf-8 -*-

import re
import string


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
        sentence = self.remove_diacritics(sentence)
        sentence = sentence.lower()
        sentence = self.remove_punctuation(sentence)
        sentence = self.custom_strip(sentence)
        return sentence

    def custom_strip(self, sentence):
        return sentence.strip("-" + string.whitespace)

    def remove_punctuation(self, sentence):
        sentence = re.sub("[:;,\.\?!]", '', sentence)
        sentence = re.sub("[\"\(\)]", '', sentence)
        return sentence

    def remove_diacritics(self, sentence):
        # a
        sentence = sentence.replace(u'á', 'a')
        sentence = sentence.replace(u'à', 'a')
        sentence = sentence.replace(u'ã', 'a')
        sentence = sentence.replace(u'â', 'a')
        # e
        sentence = sentence.replace(u'é', 'e')
        sentence = sentence.replace(u'è', 'e')
        sentence = sentence.replace(u'ẽ', 'e')
        sentence = sentence.replace(u'ê', 'e')
        # i
        sentence = sentence.replace(u'í', 'i')
        sentence = sentence.replace(u'ì', 'i')
        sentence = sentence.replace(u'ĩ', 'i')
        sentence = sentence.replace(u'î', 'i')
        # o
        sentence = sentence.replace(u'ó', 'o')
        sentence = sentence.replace(u'ò', 'o')
        sentence = sentence.replace(u'ô', 'o')
        sentence = sentence.replace(u'õ', 'o')
        # u
        sentence = sentence.replace(u'ú', 'u')
        sentence = sentence.replace(u'ù', 'u')
        sentence = sentence.replace(u'ũ', 'u')
        sentence = sentence.replace(u'û', 'u')
        # c
        sentence = sentence.replace(u'ç', 'c')

        # A
        sentence = sentence.replace(u'Á', 'A')
        sentence = sentence.replace(u'À', 'A')
        sentence = sentence.replace(u'Ã', 'A')
        sentence = sentence.replace(u'Â', 'A')

        # E
        sentence = sentence.replace(u'É', 'E')
        sentence = sentence.replace(u'È', 'E')
        sentence = sentence.replace(u'Ê', 'E')
        sentence = sentence.replace(u'Ẽ', 'E')

        # I
        sentence = sentence.replace(u'Í', 'I')
        sentence = sentence.replace(u'Ì', 'I')
        sentence = sentence.replace(u'Î', 'I')
        sentence = sentence.replace(u'Ĩ', 'I')

        # O
        sentence = sentence.replace(u'Ó', 'O')
        sentence = sentence.replace(u'Ò', 'O')
        sentence = sentence.replace(u'Õ', 'O')
        sentence = sentence.replace(u'Ô', 'O')

        # U
        sentence = sentence.replace(u'Ú', 'U')
        sentence = sentence.replace(u'Ù', 'U')
        sentence = sentence.replace(u'Û', 'U')
        sentence = sentence.replace(u'Ũ', 'U')

        # C
        sentence = sentence.replace(u'Ç', 'C')
        return sentence
