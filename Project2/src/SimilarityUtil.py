# -*- coding: utf-8 -

import nltk
from BigramForestTagger import BigramForestTagger
from nltk.tokenize import wordpunct_tokenize


def jaccard_sentence(sentence1, sentence2):
    """
    Determines jaccard ratio of two sentences

    :param sentence1:
    :param sentence2:
    :return: jaccard value
    """
    return jaccard(wordpunct_tokenize(sentence1), wordpunct_tokenize(sentence2))


def jaccard(sequence1, sequence2):
    """
    Determines jaccard ratio of two lists

    :param sequence1: first list
    :param sequence2: second list
    :return: jaccard value
    """
    s1, s2 = set(sequence1), set(sequence2)
    intersection = s1.intersection(s2)

    return float(len(intersection)) / float((len(s1) + len(s2) - len(intersection)))


def dice(sequence1, sequence2):
    """

    :param sequence1:
    :param sequence2:
    :return: dice value
    """
    s1, s2 = set(sequence1), set(sequence2)
    intersection = s1.intersection(s2)
    return 2*(float(len(intersection)) / float((len(s1) + len(s2))))


def dice_sentence(sentence1, sentence2):
    """

    :param sentence1:
    :param sentence2:
    :return: dice value
    """
    return dice(wordpunct_tokenize(sentence1), wordpunct_tokenize(sentence2))


def med_sentence(sentence1, sentence2, c1=1, c2=1, c3=1):
    """
    Determines minimum edit distance of two sentences. No normalization is done

    :param sentence1: first sentence
    :param sentence2: second sentence
    :param c1: optional weight
    :param c2: optional weight
    :param c3: optional weight
    :return: integer, minimum edit distance
    """
    sequence1 = wordpunct_tokenize(sentence1)
    sequence2 = wordpunct_tokenize(sentence2)

    return med(sequence1, sequence2, c1, c2, c3)


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

    if size1 == 0:
        return size2
    if size2 == 0:
        return size1

    matrix_row_size = size1 + 1
    matrix_col_size = size2 + 1

    #init size
    matrix = [None] * matrix_row_size
    for i in range(matrix_row_size):
        matrix[i] = [None] * matrix_col_size

    #init first row
    for i in range(matrix_row_size):
        matrix[i][0] = i

    #init first column
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
    result = []
    for word in sentence.split(" "):
        if word not in list_words_to_remove:
            result.append(word)
    return " ".join(result)


def filter_non_interrogative_sentence(sentence):
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
    result = []
    l = nltk.word_tokenize(sentence)
    stemmer = nltk.stem.RSLPStemmer()
    # decode porque so alguns tem u'ola', encode para tirar os malditos u
    for word in l:
        result.append(stemmer.stem(word))
    return " ".join(result)

def custom_jaccard(sentence1, sentence2, tagger, weighttag = 0.5):

    tagged_sentence1 = tagger.tag_sentence(sentence1)
    tagged_sentence2 = tagger.tag_sentence(sentence2)

    s1, s2 = set(tagged_sentence1), set(tagged_sentence2)

    intersection = s1.intersection(s2)

    non_intersection1 = s1.difference(s2)
    non_intersection2 = s2.difference(s1)

    taglist1 = extract_tags(non_intersection1)
    taglist2 = extract_tags(non_intersection2)

    tag_set1, tag_set2 = set(taglist1), set(taglist2)
    tag_intersection = tag_set1.intersection(tag_set2)

    jaccardlength = float((len(s1) + len(s2) - len(intersection)))

    jaccarda = float(len(intersection))
    #dividing by the corresponding size
    jaccardb = weighttag * float(len(tag_intersection))


    #tag = get_tag(word1)
    #if tag in ['n', 'art', 'prp', 'prop', 'pron-pers', 'pron-det', 'pron-indp', 'num', ' '

    return (jaccarda + jaccardb) / jaccardlength


def extract_tags(non_intersection):
    taglist = list()
    for word in non_intersection:
        taglist.append(get_tag(word))
    return taglist


def get_tag(word):
    return word[1]

def same_tag(tagged_word1, tagged_word2):
    return tagged_word1[1] == tagged_word2[1]


def filter_tags(list_pairs_token_tag, tags_to_remove):
    result = []
    for el in list_pairs_token_tag:
        if el[1] not in tags_to_remove:
            result.append(el)

    return result



if __name__ == '__main__':
    a=[('O', 'n'), ('Bruno', 'n'), ('sujou', 'n'), ('a', u'prp'), ('careca', 'n'), ('!', u'!')]
    b=[('A', 'n'), ('Bruna', 'n'), ('sujou', 'n'), ('a', u'prp'), ('cabeleira', 'n'), ('!', u'!')]
    print extract_tags(a)
    print '\n'
    print jaccard_sentence(r"O Bruno sujou a careca!", r"A Bruna sujou a cabeleira!")
    print custom_jaccard(r"O Bruno sujou a careca!", r"A Bruna sujou a cabeleira!")











