def jaccard(v1, v2):
    s1, s2 = set(v1), set(v2)
    intersection = s1.intersection(s2)
    return float(len(intersection)) / float((len(s1) + len(s2) - len(intersection)))

def dice(v1, v2):
    s1, s2 = set(v1), set(v2)
    intersection = s1.intersection(s2)
    return 2*(float(len(intersection)) / float((len(s1) + len(s2))))


def word_to_list_chars(word):
    return list(word)