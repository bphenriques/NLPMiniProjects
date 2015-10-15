# -*- coding: utf-8 -*-

import re
import string


class RegexUtil:
    WHITE_SPACE = "\s"
    PT_LETTER = "À-ÿ\w"
    PUNCTUATION = ":;,\.\?!\"\(\)"

    @staticmethod
    def normalize_string(sentence):
        sentence = RegexUtil.remove_diacritics(sentence)
        sentence = sentence.lower()
        sentence = RegexUtil.remove_punctuation(sentence)
        sentence = RegexUtil.custom_strip(sentence)
        return sentence

    @staticmethod
    def custom_strip(sentence):
        return sentence.strip("-" + string.whitespace)

    @staticmethod
    def remove_punctuation(sentence):
        return re.sub("[" + RegexUtil.PUNCTUATION + "]", '', sentence)

    @staticmethod
    def remove_diacritics(sentence):
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
