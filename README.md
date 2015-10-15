# Neuro Linguistic Programming Mini Projects

Mini projects done for Natural Linguistic programming in Instituto Superior Técnico, Tagus-park, Oeiras.
There are two folders:
- Project 1
- Project 2

The project aims to, in the portuguese language, given a question deliver the most probable answer.

## Example usage

A file "example.py" shows an example of code usage:

```sh
$ python
```

```python
from Interface import sss
from Interface import myAvalia

corpus_src = "TestResources/PerguntasPosSistema.txt"

question_1 = "A tua familia é numerosa?"
print "Q: ", question_1 
print "R: ", sss(corpus_src, question_1) # Não sei responder

question_2 = "Tens filhos?"
print "Q: ", question_1
print "R: ", sss(corpus_src, question_2) # Não.

print ""

accuracy = myAvalia("TestResources/AnotadoAll.txt", "TestResources/Perguntas.txt", "TestResources/PerguntasPosSistema.txt")
print "Perguntas.txt accuracy is: ", accuracy # 0.333333
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
[Bruno Henriques]: <https://github.com/bphenriques>
[Tiago Santos]: <https://github.com/GitTiago>
