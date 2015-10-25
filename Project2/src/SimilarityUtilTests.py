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


if __name__ == "__main__":
    tests = [
        test_jaccard,
        test_dice
    ]

    run_tests(tests)
