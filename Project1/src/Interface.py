# -*- coding: utf-8 -
from AnswerPicker import AnswerPicker
from AnnotationCheck import AnnotationCheck


def sss(file_name, question):
    trigger_answer_reader = AnswerPicker()
    trigger_answer_reader.process_file(file_name)
    return trigger_answer_reader.get_answer(question)


def myAvalia(annotation_file, questions_file, corpus_file_path="TestResources/PerguntasPosSistema.txt", ):
    questions_answers_reader = AnswerPicker()
    questions_answers_reader.process_file(corpus_file_path)

    annotation_check = AnnotationCheck(annotation_file)
    accuracy = annotation_check.evaluate_accuracy(questions_answers_reader, questions_file, 20)

    return accuracy
