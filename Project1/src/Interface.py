# -*- coding: utf-8 -
from AnswerPicker import AnswerPicker
from AnnotationCheck import AnnotationCheck
from AnswerPicker import AnswerPickerAnswerResult

INVALID_USER_INPUT = u"Frase incorrecta"
TRIGGER_NOT_FOUND = u"Não sei responder"


def sss(file_name, question):
    # process corpus file
    trigger_answer_reader = AnswerPicker()
    trigger_answer_reader.process_file(file_name)

    # getting the answer
    answer = trigger_answer_reader.get_answer(question)
    if answer == AnswerPickerAnswerResult.INVALID_USER_INPUT:
        return INVALID_USER_INPUT
    elif answer == AnswerPickerAnswerResult.TRIGGER_NOT_FOUND:
        return TRIGGER_NOT_FOUND

    return answer


def myAvalia(annotation_file, questions_file, corpus_file_path="TestResources/PerguntasPosSistema.txt", ):
    # process corpus file
    questions_answers_reader = AnswerPicker()
    questions_answers_reader.process_file(corpus_file_path)

    # analyse annotation_file and return the accuracy
    annotation_check = AnnotationCheck(annotation_file)
    accuracy = annotation_check.evaluate_accuracy(questions_answers_reader, questions_file, 20)

    return accuracy
