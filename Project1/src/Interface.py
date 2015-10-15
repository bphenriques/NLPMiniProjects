# -*- coding: utf-8 -
from TriggersAnswerReader import TriggersAnswerReader
from AnnotationCheck import AnnotationCheck

def sss(file_name, question):
    trigger_answer_reader = TriggersAnswerReader()
    trigger_answer_reader.process_file(file_name)
    #trigger_answer_reader.dump_map()
    answer = trigger_answer_reader.get_answer(question)
    if answer is None:
        answer = "Não sei responder"
    return answer.decode("utf-8")

def myAvalia(annotation_file, questions_file):
    questions_answers_reader = TriggersAnswerReader()
    #Todo: filepath bad! bad hardcoding, down boy!
    questions_answers_reader.process_file("TestResources/PerguntasPosSistema.txt")

    annotation_check = AnnotationCheck(annotation_file)
    answers_list = annotation_check.your_avalia(questions_answers_reader, questions_file, 20)

    return annotation_check.accuracy(answers_list)

def test_sss():
    print "--- TESTING sss ---"

    # The following question has no triggers that are similar to the user input
    assert sss("TestResources/PerguntasPosSistema.txt", "A tua familia é numerosa?") == u"Não sei responder"

    #Non existent at all
    assert sss("TestResources/PerguntasPosSistema.txt", "I DONT EXIST?") == u"Não sei responder"

    #There are many similar triggers with this user_input
    assert sss("TestResources/PerguntasPosSistema.txt", "Tens filhos?") == u"Não."
    assert sss("TestResources/PerguntasPosSistema.txt", "tens filhos?") == u"Não sei responder"

    print "--- PASSED sss tests ---"

def test_myAvalia():
    print "--- TESTING myAvalia ---"
    assert myAvalia("../txt/AnotadoAll.txt", "TestResources/Perguntas.txt") == (float(1)/3)
    print "--- PASSED myAvalia tests ---"


if __name__ == "__main__":
    test_sss()
    test_myAvalia()

    print "Passed sss tests"
