
from pymystem3 import Mystem
import pandas as pd
df3 = pd.read_csv('info.csv', delimiter=';', encoding='1251')
end = ""

df2 = pd.read_csv('mystem_info2.csv', delimiter=';', encoding='1251')
print(df2)
df4 = pd.read_csv('mystem_info.csv', delimiter=';', encoding='1251')
print(df4)
# for i in df3["name"]:
#     text_string = i.lower()
#     a = []
#     D = ""
#     l = {}
#     a = text_string.split(';')
#     m = Mystem()
#     n = len(a)
#     j = 0
#     for s in a:
#         lemmas = m.lemmatize(s)
#         for lemma in lemmas:
#             if (lemma.isalpha() == True):
#                 D += lemma + " "
#     D=D[:len(D)-1]
#     end=end+D+";"
#     print(end)
