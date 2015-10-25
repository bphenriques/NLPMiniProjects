def jaccard_sentence(s1, s2):
    return jaccard(s1.split(' '), s2.split(' '))


def jaccard(v1, v2):
    s1, s2 = set(v1), set(v2)
    intersection = s1.intersection(s2)

    return float(len(intersection)) / float((len(s1) + len(s2) - len(intersection)))

def dice(v1, v2):
    s1, s2 = set(v1), set(v2)
    intersection = s1.intersection(s2)
    return 2*(float(len(intersection)) / float((len(s1) + len(s2))))

def dice_sentence(s1, s2):
    return dice(s1.split(' '), s2.split(' '))

def MED(sentence1, sentence2, c1=1, c2=1, c3=1):
    size1, size2 = len(sentence1), len(sentence2)

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
        word1 = sentence1[i - 1]
        for j in range(1, matrix_col_size):
            word2 = sentence2[j - 1]
            if word1 == word2:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = min(matrix[i-1][j] + c1, matrix[i][j-1] + c2, matrix[i-1][j-1] + c3)

    return matrix[matrix_row_size - 1][matrix_col_size - 1]


