from pymystem3 import Mystem
import pandas as pd

document_text = input()
text_string = document_text.lower()
df3 = pd.read_csv('info.csv', delimiter=';', encoding='1251')
df = pd.read_csv('new.csv', delimiter=';', encoding='1251')
df2 = pd.read_csv('mystem_info.csv', delimiter=';', encoding='1251')
faculty = list()
test = set()


def mystem_sentence(document_text):  # частотный словарь начальных форм (для поиска вопроса)
    text_string = document_text.lower()
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
    return D


def question_from_user(sentence, a): # поиск нужных данных
    for i in sentence.split():
        print(i)
        if i in a:
            return True
    return False

def mystem_words(document_text): # частотный словарь начальных форм (для поиска факультета)
    text_string = document_text.lower()
    a = []
    D = ""
    l = {}
    a = text_string.split(';')
    m = Mystem()
    n = len(a)
    j = 0
    for s in a:
        lemmas = m.lemmatize(s)
        for lemma in lemmas:
            if (lemma.isalpha() == True):
                D += lemma + " "

    return D


def search_faculty(document_text):
    for names in df2:  # создаем список множеств факультетов
        faculty.append(set(names.split(" ")))
    for i in faculty:# убираем ненужные слова
        for a in i.copy():
            if len(a) < 3:
                i.remove(a)
    text_string = mystem_words(document_text)  # создаем предложение, состоящее из начальных форм предложения пользователя
    words = set()
    for word in text_string.split(" "):  # добавляем слова введенные пользователем (нач формы) в множество
        words.add(word)
    maximal = dict() # cловарь максимальных совпадений
    for i in range(len(faculty)): # для каждого факультета
        if not faculty[i].isdisjoint(words):  # проверяет общие элементы
            maximal[i] = faculty[i].intersection(words) # пересечение множеств факультетов и предложения пользователя
    maximal = list(maximal.items()) # преобразование в список для дальнейшего поиска максимальных совпадений
    try:
        out = []
        a = max(maximal, key=lambda i: i[1]) # поиск максимального элемента в списке
        for i in range(len(maximal)):
            if len(maximal[i][1]) == len(a[1]): # првоерка на то что максимальных элементов несколько
                out.append(df3.iloc[maximal[i][0]]['Название']) # добавление этих элементов в вывод
        return out
    except:
        print("Направление не найдено")

D = mystem_sentence(document_text)
sentence = ""
for key in D.keys(): #делаем предложение, состоящие из начальных форм слов пользователя
    sentence += key + " "
b=search_faculty(document_text)


def bot_sentence():
    price = ["цена", "заплатить", "плата", "стоит", "стоимость", "выйдет", "стоить"]
    if question_from_user(sentence, price):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            print(f"Цена на направлении {b[i]}: " + str(a['Цена'].values.item()))
    exam = ['сдавать', 'сдать', 'необходимо сдать', 'сдача']
    if question_from_user(sentence, exam):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            print(f"Экзамены для поступления на направление {b[i]}: " + str(a['Экз'].values.item()))
    prohodnoy = ['проходной', 'поступить', 'порог поступить', 'поступление']
    if question_from_user(sentence, prohodnoy):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            print(f"Минимальный проходной балл в прошлом году на направлении {b[i]}: " + str(
                a['Мингод'].values.item()) + ' балл(-ов).')
    zayavka = ['заявление', 'подать', 'подача', 'порог заявление']
    if question_from_user(sentence, zayavka):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            print(f"Минимальный балл на подачу заявление на поступление в прошлом году на направлении {b[i]}: " + str(
                a['Мин'].values.item()) + ' балл(-ов).')
    budget = ['бюджет', 'бюджетный', 'бюджетник', 'бюджетным']
    if question_from_user(sentence, budget):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            print(f"Количество бюджетных мест на направлении {b[i]}: " + str(a['Бюдж'].values.item()))
    tcelevoy = ['целевой', 'целевых', 'целевик', 'целевым']
    if question_from_user(sentence, tcelevoy):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            print(f"Количество целевых мест на направлении {b[i]}: " + str(a['Целевик'].values.item()))
    kvota = ['квотный', 'квотных', 'квотник', 'квотным']
    if question_from_user(sentence, kvota):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            print(f"Количество квотных мест на направлении {b[i]}: " + str(a['Квота'].values.item()))
    platn = ['платный', 'платник', 'платных', 'платным']
    if question_from_user(sentence, platn):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            print(f"Количество платных мест на направлении {b[i]}: " + str(a['Плат'].values.item()))


bot_sentence()