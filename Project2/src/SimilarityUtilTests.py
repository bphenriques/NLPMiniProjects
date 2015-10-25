from SimilarityUtil import *
from TestsUtil import run_tests

def test_jaccard():
    s = "saturday"
    t = "sunday"
    w = "day"
    assert jaccard(s, t) == float(5)/float(8)
    assert jaccard(s, w) == float(3)/float(7)

def test_dice():
    s = "saturday"
    t = "sunday"
    w = "day"
    assert dice(s, t) == float(10)/float(13)
    assert dice(s, w) == float(6)/float(10)

def test_med():
    s = 'batalha'
    t = 'barata'
    u = 'Bruno'
    w = 'bruno'
    y = 'Bruna'
    x = 'Brunoob'

    assert MED(s, t) == 3
    assert MED(t, s) == 3
    assert MED(u, w) == 1
    assert MED(u, y) == 1
    assert MED(x, u) == 2
    assert MED(x, w) == 3

if __name__ == "__main__":
    tests = [
        test_jaccard,
        test_dice,
        test_med
    ]

    run_tests(tests)
