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