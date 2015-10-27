# -*- coding: utf-8 -

from SimilarityUtil import *
from Tests.TestsUtil import run_tests

def test_jaccard_word():
    s = "saturday"
    t = "sunday"
    w = "day"
    assert jaccard(s, t) == float(5)/float(8)
    assert jaccard(s, w) == float(3)/float(7)

def test_jaccard_sentence():
    s = "eu gosto imenso de lingua natural"
    t = "de lingua natural eu gosto imenso"

    u = "Eu gosto da maria"
    v = "Eu gosto da Ana"

    assert(jaccard_sentence(s, t) == 1)
    assert(jaccard_sentence(u, v) == float(3)/float(5))

def test_dice_word():
    s = "saturday"
    t = "sunday"
    w = "day"
    assert dice(s, t) == float(10)/float(13)
    assert dice(s, w) == float(6)/float(10)

def test_dice_sentence():
    s = "eu gosto imenso de lingua natural"
    t = "de lingua natural eu gosto imenso"

    u = "Eu gosto da maria"
    v = "Eu gosto da Ana"

    assert(dice_sentence(s, t) == 1)
    assert(dice_sentence(u, v) == (2*float(3))/float(4 + 4))

def test_med():
    s = 'batalha'
    t = 'barata'
    u = 'Bruno'
    w = 'bruno'
    y = 'Bruna'
    x = 'Brunoob'

    assert med(s, t) == 3
    assert med(t, s) == 3
    assert med(u, w) == 1
    assert med(u, y) == 1
    assert med(x, u) == 2
    assert med(x, w) == 3
    assert med_sentence("A Bruna e muita linda", "O Bruno e muito lindo") == 4
    assert med_sentence("A Bruna e-muita linda", "O Bruno e muito lindo") == 5

if __name__ == "__main__":
    tests = [
        test_jaccard_word,
        test_jaccard_sentence,
        test_dice_word,
        test_dice_sentence,
        test_med
    ]

    run_tests(tests)
