import pandas as pd
from pymystem3 import Mystem

document_text = input()
text_string = document_text.lower()
df3 = pd.read_csv('info.csv', delimiter=';', encoding='1251')
df = pd.read_csv('new.csv', delimiter=';', encoding='1251')
df2 = pd.read_csv('info_short.csv', delimiter=';', encoding='1251')
D = {}
l = {}
a = text_string.split(';')
m = Mystem()
n = len(a)
j = 0

for s in a:
    lemmas = m.lemmatize(s)
    for lemma in lemmas:
        if lemma.isalpha() == True:
            l = D.get(lemma, [0] * n)
            l[j] = l[j] + 1
            D[lemma] = l
    j = j + 1
b = []
print(b)
print(D)
for i in D.keys():
    a = df[df['name'] == i]
    new_list = [item for sublist in a.values.tolist() for item in sublist]
    b.append(new_list)
    if len(new_list) == 0:
        print('asdf')
        break
    print(b)
diction = dict()
for i in range(len(b)):
    diction[i] = dict()
    diction[i] = dict(zip(list(df), b[i]))
    del diction[i]['name']



operator_main = dict()
for i in range(len(diction) + 1):
    if len(diction) == 1:
        operator_main = diction[i]
        break
    trash = diction[i]
    for key, value in trash.items():
        if key in diction[i + 1] and value == diction[i + 1][key]:
            operator_main[key] = value
        elif key in diction[i + 1] and (value > 1 and value - 1 == diction[i + 1][key]):
            operator_main[key] = value - 1
        elif key in diction[i + 1] and (value > 0 and value + 1 == diction[i + 1][key]):
            operator_main[key] = value
    if i + 2 >= len(diction):
        break
    operator_main = dict()


final_dict = {x: y for x, y in
              filter(lambda x: operator_main[x[0]] == max(operator_main.values()), operator_main.items())}

for i in final_dict.keys():
    i = int(i)
    print(df2.columns[i])
    a = df3[df3['Название'] == df2.columns[i]]
    print(a['Бюдж'].values.item())

