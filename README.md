# Neuro Linguistic Programming Mini Projects

Mini projects done for Natural Linguistic programming in Instituto Superior Técnico, Tagus-park, Oeiras.
There are two folders:
- Project 1
- Project 2

The project aims to, in the portuguese language, given a question deliver the most probable answer.

The python version used for this project is 2.7.10

## Example usage

A file in "Project1/src/example.py" shows an example of usage:

```sh
$ cd NLPMiniProjects/Project1/src
$ python
```

```python
from Interface import sss, myAvalia
from SimilarityUtil import dice_sentence
from BigramForestTagger import BigramForestTagger
import StrategiesForAnswers as sa
import StrategiesForTriggers as st

annotations_file_path = "TestResources/AnotadoAll.txt"
test_input_file = "TestResources/TestInput.txt"
corpus_file_path = "TestResources/PerguntasPosSistema.txt"

question_1 = "A tua familia é numerosa?"
print "Q: ", question_1
print "R: ", sss(corpus_file_path, question_1) # Não sei responder

print ""

question_2 = "Tens filhos?"
print "Q: ", question_1
print "R: ", sss(corpus_file_path, question_2) # Não

print ""

accuracy = myAvalia(annotations_file_path, test_input_file, corpus_file_path) # 0.0857142857143
print test_input_file, "accuracy is:", accuracy

################################
# Using custom strategies (project 2)
###############################

tagger = BigramForestTagger()  # training corpus floresta
tagger.train()

trigger_strategy = st.Braccard(tagger, 0.25, 0.50, True)
answer_strategy = sa.YesNoSimilar(0.75, 0.5, dice_sentence, True)

question_1 = "A tua familia é numerosa?"
print "Q: ", question_1
print "R: ", sss(corpus_file_path, question_1, trigger_strategy, answer_strategy) # Não é isso...

print ""

accuracy = myAvalia(annotations_file_path, test_input_file, corpus_file_path, trigger_strategy, answer_strategy)
print test_input_file, "accuracy is:", accuracy # 0.428571428571
```

# File Structure
### Corpus file
```
...
User Input - Viste o último filme do Woody Allen?
	A - Não é nada oficial ainda, eu não dei a minha palavra ainda. : n
	A - Eu não entendi patavina. : m
	A - De qual filme estás a falar? : y
	...
User Input - És de onde?
    ...
```

### Anotations file
```
...
User Input: A tua familia é numerosa?
T - A tua família?
A - Não é isso...
...
```

### Questions file
```
A tua familia é numerosa?
Aceitas tomar café?
Andas na escola?
```

# Urls

* [Natural Language Toolkit]
* [Tiago Santos]
* [Bruno Henriques]

[Natural Language Toolkit]: <http://www.nltk.org/>
[Corpus Floresta examples]: <http://www.nltk.org/howto/portuguese_en.html>
[Corpus Floresta Symbols]: <http://beta.visl.sdu.dk/visl/pt/symbolset-floresta.html>
[Bruno Henriques]: <https://github.com/bphenriques>
[Tiago Santos]: <https://github.com/GitTiago>
