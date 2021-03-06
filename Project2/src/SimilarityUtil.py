# -*- coding: utf-8 -

import nltk
from nltk.tokenize import wordpunct_tokenize


def jaccard_sentence(sentence1, sentence2):
    """
    Determines jaccard value of two sentences

    :param sentence1:
    :param sentence2:
    :return: jaccard value
    """
    return jaccard(wordpunct_tokenize(sentence1), wordpunct_tokenize(sentence2))


def jaccard(sequence1, sequence2):
    """
    Determines Jaccard value of two lists

    :param sequence1: first list
    :param sequence2: second list
    :return: jaccard value
    """
    s1, s2 = set(sequence1), set(sequence2)
    intersection = s1.intersection(s2)

    aux = len(s1) + len(s2) - len(intersection)
    if aux == 0: return 1

    return float(len(intersection)) / float(aux)


def dice(sequence1, sequence2):
    """
    Determines the Dice value of two lists

    :param sequence1:
    :param sequence2:
    :return: dice value
    """
    s1, s2 = set(sequence1), set(sequence2)
    if len(s1) == 0 or len(s2) == 0: return 0

    intersection = s1.intersection(s2)
    return 2*(float(len(intersection)) / float((len(s1) + len(s2))))


def dice_sentence(sentence1, sentence2):
    """
    Determines the Dice value of two sentences

    :param sentence1:
    :param sentence2:
    :return: dice value
    """
    return dice(wordpunct_tokenize(sentence1), wordpunct_tokenize(sentence2))


def med_sentence(sentence1, sentence2, c1=1, c2=1, c3=1):
    """
    Determines minimum edit distance of two sentences.

    :param sentence1: first sentence
    :param sentence2: second sentence
    :param c1: optional weight
    :param c2: optional weight
    :param c3: optional weight
    :return: integer, minimum edit distance
    """

    return med(wordpunct_tokenize(sentence1), wordpunct_tokenize(sentence2), c1, c2, c3)


def med(sequence1, sequence2, c1=1, c2=1, c3=1):
    """
    Determines minimum edit distance of two sequences.

    :param sequence1: first list
    :param sequence2: second list
    :param c1: optional weight
    :param c2: optional weight
    :param c3: optional weight
    :return: integer, minimum edit distance
    """
    size1, size2 = len(sequence1), len(sequence2)

    if size1 == 0: return size2
    if size2 == 0: return size1

    matrix_row_size, matrix_col_size = size1 + 1, size2 + 1

    # init size
    matrix = [None] * matrix_row_size
    for i in range(matrix_row_size):
        matrix[i] = [None] * matrix_col_size

    # init first row
    for i in range(matrix_row_size):
        matrix[i][0] = i

    # init first column
    for j in range(matrix_col_size):
        matrix[0][j] = j

    for i in range(1, matrix_row_size):
        element1 = sequence1[i - 1]
        for j in range(1, matrix_col_size):
            element2 = sequence2[j - 1]
            if element1 == element2:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = min(matrix[i-1][j] + c1,
                                   matrix[i][j-1] + c2,
                                   matrix[i-1][j-1] + c3)

    return matrix[matrix_row_size - 1][matrix_col_size - 1]


def remove_stop_words(sentence, list_words_to_remove = nltk.corpus.stopwords.words('portuguese')):
    """
    Remove stop words of a sentence
    :param sentence:
    :param list_words_to_remove: default is the list from nltk corpus for portuguese language.
    :return: sentence with the stop words removed
    """
    result = []
    for word in sentence.split(" "):
        if word.lower() in list_words_to_remove:
            continue
        result.append(word)
    return " ".join(result)


def filter_non_interrogative_sentence(sentence):
    """
    Remove non-interrogative sentences so sentences like "Optimo. Vamos para la?" become "Vamos para la'"
    It is assumed that interrogative sentence can end with "?" or "..."

    :param sentence:
    :return: sentence filtered
    """
    split = [sentence]

    if "!" in sentence:
        split = sentence.split("!")
    elif "..." in sentence:
        return sentence
    elif "." in sentence:
        split = sentence.split(".")
    else:
        return sentence

    return split[len(split)-1].strip()


def tok_stem(sentence):
    """
    Stem with all the words stemmed
    :param sentence:
    :return: Sentence with all the words stemmed
    """
    result = []
    l = nltk.word_tokenize(sentence)
    stemmer = nltk.stem.RSLPStemmer()

    for word in l:
        result.append(stemmer.stem(word))
    return " ".join(result)

def custom_jaccard(sentence1, sentence2, tagger, weighttag):
    """
    Custom version of jaccard with a morphological component

    :param sentence1:
    :param sentence2:
    :param tagger: tagger
    :param weighttag: weight of the tagging component
    :return:
    """

    tagged_sentence1 = tagger.tag_sentence(sentence1)
    tagged_sentence2 = tagger.tag_sentence(sentence2)

    s1, s2 = set(tagged_sentence1), set(tagged_sentence2)
    if len(s1) == 0 and len(s2) == 0:
        return 0

    intersection = s1.intersection(s2)

    non_intersection1 = s1.difference(s2)
    non_intersection2 = s2.difference(s1)

    taglist1 = extract_tags(non_intersection1)
    taglist2 = extract_tags(non_intersection2)

    tag_set1, tag_set2 = set(taglist1), set(taglist2)
    tag_intersection = tag_set1.intersection(tag_set2)

    jaccardlength = float((len(s1) + len(s2) - len(intersection)))

    jaccarda = float(len(intersection))
    # dividing by the corresponding size
    jaccardb = weighttag * float(len(tag_intersection))


    #tag = get_tag(word1)
    #if tag in ['n', 'art', 'prp', 'prop', 'pron-pers', 'pron-det', 'pron-indp', 'num', ' '

    return (jaccarda + jaccardb) / jaccardlength


def similar_yes_no(s1, s2, weight, weight_func):
    """
    If s1 s2 contains both "sim" or "nao" then weight + (1-weight) * weight_func(s1,s2)
    else returns weight_func(s1,s2)

    :param s1:
    :param s2:
    :param weight: weight
    :param weight_func: similarity weight function (jaccard_sentence or dice_sentence)
    :return:
    """
    if ('sim' in s1 and 'sim' in s2) or ('nao' in s1 and 'nao' in s2):
        return (1 - weight) * weight_func(s1, s2) + weight
    else:
        return weight_func(s1, s2)


def extract_tags(non_intersection):
    taglist = list()
    for word in non_intersection:
        taglist.append(get_tag(word))
    return taglist


def get_tag(word):
    """
    Returns the tag of te tuple
    :param word:
    :return: the tag
    """
    return word[1]

def same_tag(tagged_word1, tagged_word2):
    """
    Checks if two tagged words have the same tag
    :param tagged_word1:
    :param tagged_word2:
    :return: true if both words have the same tag
    """
    return tagged_word1[1] == tagged_word2[1]


def filter_tags(list_pairs_token_tag, tags_to_remove):
    """
    Remove the words that have the tag contained in the list tags_to_remove
    :param list_pairs_token_tag:
    :param tags_to_remove:
    :return: filtered sentence
    """
    result = []
    for el in list_pairs_token_tag:
        if get_tag(el) in tags_to_remove:
            continue
        result.append(el)

    return result



if __name__ == '__main__':
    a=[('O', 'n'), ('Bruno', 'n'), ('sujou', 'n'), ('a', u'prp'), ('careca', 'n'), ('!', u'!')]
    b=[('A', 'n'), ('Bruna', 'n'), ('sujou', 'n'), ('a', u'prp'), ('cabeleira', 'n'), ('!', u'!')]
    print extract_tags(a)
    print '\n'
    print tok_stem(u"A MARIA É MUITO BONITA")

    # print jaccard_sentence(r"O Bruno sujou a careca!", r"A Bruna sujou a cabeleira!")











