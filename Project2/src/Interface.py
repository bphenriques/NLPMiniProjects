# -*- coding: utf-8 -

from AnswerPicker import AnswerPicker
from AnnotationCheck import AnnotationCheck
from AnswerPicker import AnswerPickerAnswerResult
from UserInputTriggerAnswerReader import UserInputTriggerAnswerReader

INVALID_USER_INPUT = u"Frase incorrecta"
TRIGGER_NOT_FOUND = u"Não percebi"


def sss(file_name, question, trigger_strategy=None, answer_strategy=None):
    """
    Returns the most appropriate answer for a question

    :param file_name: corpus file
    :param question: question
    :param trigger_strategy:  optional. Strategy for comparing User Input and Trigger
    :param answer_strategy:  optional. Strategy for comparing answers
    :return: The most appropriate answer for the question
    """
    # process corpus file
    file_reader = UserInputTriggerAnswerReader()
    answer_picker = AnswerPicker(file_reader, trigger_strategy, answer_strategy)
    file_reader.process_file(file_name, answer_picker.process_user_input_answer)

    # getting the answer
    answer = answer_picker.get_answer(question)
    if answer == AnswerPickerAnswerResult.INVALID_USER_INPUT:
        return INVALID_USER_INPUT
    elif answer == AnswerPickerAnswerResult.TRIGGER_NOT_FOUND:
        return TRIGGER_NOT_FOUND

    return answer


def myAvalia(annotation_file, questions_file, corpus_file_path="TestResources/PerguntasPosSistema.txt", trigger_strategy=None, answer_strategy=None):
    """
    :param annotation_file: annotated file
    :param questions_file: list of questions file path
    :param corpus_file_path: corpus file path
    :param trigger_strategy: optional. Strategy for comparing User Input and Trigger
    :param answer_strategy: optional. Strategy for comparing answers
    :return: accuracy of the system
    """

    # process corpus file
    file_reader = UserInputTriggerAnswerReader()
    answer_picker = AnswerPicker(file_reader, trigger_strategy, answer_strategy)
    file_reader.process_file(corpus_file_path, answer_picker.process_user_input_answer)

    # analyse annotation_file and return the accuracy
    annotation_check = AnnotationCheck(annotation_file)
    accuracy = annotation_check.evaluate_accuracy(answer_picker, questions_file, 20)

    return accuracy
