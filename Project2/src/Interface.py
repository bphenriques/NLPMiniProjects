# -*- coding: utf-8 -

from AnswerPicker import AnswerPicker
from AnnotationCheck import AnnotationCheck
from AnswerPicker import AnswerPickerAnswerResult
from UserInputTriggerAnswerReader import UserInputTriggerAnswerReader

INVALID_USER_INPUT = u"Frase incorrecta"
TRIGGER_NOT_FOUND = u"Não sei responder"


def sss(file_name, question):
    # process corpus file
    file_reader = UserInputTriggerAnswerReader()
    answer_picker = AnswerPicker(file_reader)

    file_reader.process_file(file_name, answer_picker.process_user_input_answer)

    # getting the answer
    answer = answer_picker.get_answer(question)
    if answer == AnswerPickerAnswerResult.INVALID_USER_INPUT:
        return INVALID_USER_INPUT
    elif answer == AnswerPickerAnswerResult.TRIGGER_NOT_FOUND:
        return TRIGGER_NOT_FOUND

    return answer


def myAvalia(annotation_file, questions_file, corpus_file_path="TestResources/PerguntasPosSistema.txt", strategy=None):
    # process corpus file
    file_reader = UserInputTriggerAnswerReader()
    answer_picker = AnswerPicker(file_reader, strategy)
    file_reader.process_file(corpus_file_path, answer_picker.process_user_input_answer)

    # analyse annotation_file and return the accuracy
    annotation_check = AnnotationCheck(annotation_file)
    accuracy = annotation_check.evaluate_accuracy(answer_picker, questions_file, 20)

    return accuracy