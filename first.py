import pandas as pd
from pymystem3 import Mystem

document_text = open('questions.csv', 'r')
text_string = document_text.read().lower()

a = []
D = {}
l = {}
a = text_string.split(';')
m = Mystem()
n = len(a)
j = 0
for s in a:
    lemmas = m.lemmatize(s)
    for lemma in lemmas:
        if (lemma.isalpha() == True):
            l = D.get(lemma, [0] * n)
            l[j] = l[j] + 1
            D[lemma] = l
    j = j + 1
asd = pd.DataFrame.from_dict(D, orient='index')
asd.to_csv('mystemquestions.csv', sep=';', encoding='ANSI')
file = pd.read_csv('mystemquestions.csv', encoding='ANSI', sep=';')
