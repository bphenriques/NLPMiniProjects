# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import floresta


class BigramForestTagger:

    __tagger = None
    __is_trained = False
    __corpus = None

    def __init__(self, tsents=floresta.tagged_sents()):
        self.__corpus = tsents

    def train(self):
        tsents = [[(w.lower(), self._simplify_tag(t)) for (w, t) in sent] for sent in self.__corpus if sent]
        train = tsents[100:]
        tagger0 = nltk.DefaultTagger('n')
        tagger1 = nltk.UnigramTagger(train, backoff=tagger0)
        self.__tagger = nltk.BigramTagger(train, backoff=tagger1)
        self.__is_trained = True

    def tag_sentence(self, sentence):
        if not self.__is_trained:
            self.train()
        tagged_sentence = self.__tagger.tag(nltk.word_tokenize(sentence))
        return tagged_sentence

    def _simplify_tag(self, t):
        if "+" in t:
            return t[t.index("+")+1:]
        else:
            return t

if __name__ == '__main__':
    tagger = BigramForestTagger()
    print tagger.tag_sentence(r"O Bruno sujou a careca!")

