import telebot
import pandas as pd
from pymystem3 import Mystem

bot = telebot.TeleBot(token='1694618937:AAF1ZWyYK5fuHcUIZx8CGRCyGtDEsBlPxqY')
df3 = pd.read_csv('info.csv', delimiter=';', encoding='1251')
df2 = pd.read_csv('mystem_info2.csv', delimiter=';', encoding='1251')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет, я помогу тебе узнать информацию про выбранное направление, для этого задай вопрос в виде: <вопрос> <направление>",
                 reply_markup=None)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Что я могу:\n-) Показать общее количество мест"
                 "\n-) Показать количество бюджетных, платных, квотных и целевых мест" 
                 "\n-) Указать, какие документы нужны для поступления"
                 "\n-) Экзамены необходимые для поступления"
                 "\n-) Цена обучения"
                 "\n-) Минимальные баллы в прошлом году, проходные баллы"
                 "\n-) Какой был конкурс на место в прошлом году\n\n"
                 "*В конце каждого вопроса указывайте название направления*",
                 reply_markup=None, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)  # основная функция отправки сообщений
def main(message):
    user_id = message.chat.id
    f = open('database.txt', 'a', encoding='utf=8')
    if message.text is None:
        bot.send_message(user_id, 'Пожалуйста введите вопрос, связанный с поступлением')
    else:
        document_text = {user_id: message.text}
        text_string = document_text[user_id].lower()

        # Делаем предложение, состоящие из начальных форм слов пользователя
        D = mystem_sentence(document_text[user_id])
        sentence = ""
        for key in D.keys():
            sentence += key + " "
        b = search_faculty(document_text[user_id], message)
        if b is None:
            database = {user_id: ["Отправлен NoneType", "NoneType"]}
            f.write(str(database) + "\n")
            return main
        if len(b) < 1:
            database = {user_id: ["Отправлен NoneType", "NoneType"]}
            f.write(str(database) + "\n")
            return main
        ans = bot_sentence(sentence, b, message)

        # Отправка смски
        for i in range(len(ans[user_id])):

            try:
                bot.send_message(user_id, ans[user_id][i])
                database = {user_id: [message.text, ans[user_id][i]]}
                f.write(str(database) + "\n")
            except:
                database = {user_id: ["Отправлен NoneType", ans[user_id][i]]}
                f.write(str(database) + "\n")


def mystem_sentence(document_text):  # частотный словарь начальных форм (для поиска вопроса)
    text_string = document_text.lower()
    D = {}
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


def mystem_words(document_text):  # частотный словарь начальных форм (для поиска факультета)
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


def search_faculty(document_text, message):
    user_id = message.chat.id
    faculty = list()
    for names in df2:  # создаем список множеств факультетов
        faculty.append(set(names.split(" ")))
    for i in faculty:  # убираем ненужные слова
        for a in i.copy():
            if len(a) < 3:
                i.remove(a)
    text_string = mystem_words(
        document_text)  # создаем предложение, состоящее из начальных форм предложения пользователя
    words = set()
    for word in text_string.split(" "):  # добавляем слова введенные пользователем (нач формы) в множество
        words.add(word)
    maximal = dict()  # cловарь максимальных совпадений
    for i in range(len(faculty)):  # для каждого факультета
        if not faculty[i].isdisjoint(words):  # проверяет общие элементы
            maximal[i] = faculty[i].intersection(words)  # пересечение множеств факультетов и предложения пользователя
    maximal = list(maximal.items())  # преобразование в список для дальнейшего поиска максимальных совпадений
    try:
        out = []
        a = max(maximal, key=lambda i: i[1])  # поиск максимального элемента в списке
        for i in range(len(maximal)):
            if len(maximal[i][1]) == len(a[1]):  # првоерка на то что максимальных элементов несколько
                out.append(df3.iloc[maximal[i][0]]['Название'])  # добавление этих элементов в вывод
        words = set()
        return out
    except:
        if message.text is not None:
            bot.send_message(user_id,
                             "Повторите еще раз вопрос\nВозможные проблемы:\n-) Некорректно указан вопрос\n-) Неправильно введено направление")
            # Приколы с базой данных
            f = open('database.txt', 'a')
            # Отправка смски
            database = {user_id: [message.text,
                                  "Повторите еще раз вопрос\nВозможные проблемы:\n-)Некорректно указан вопрос\n-)Неправильно введено направление"]}
            f.write(str(database) + "\n")
        else:
            bot.send_message(user_id, "Введите текст")


def question_from_user(sentence, a):  # поиск нужных данных
    for i in sentence.split():
        if i in a:
            return True
    return False


def bot_sentence(sentence, b, message):
    answers = dict()  # словарь с ответами бота
    user_id = message.chat.id
    answers[user_id] = list()  # ответы бота для каждого пользователя
    price = ["цена", "заплатить", "плата", "стоит", "стоимость", "выйдет", "стоить"]

    if b is None:
        answers[user_id].append(f"Введите направление")
        return answers
    if len(b) < 1:
        answers[user_id].append(f"Введите направление")
        return answers
    if question_from_user(sentence, price):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(f"Цена на направлении {b[i]}: " + str(a['Цена'].values.item()))

    exam = ['сдавать', 'сдать', 'необходимо сдать', 'сдача']
    if question_from_user(sentence, exam):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(f"Экзамены для поступления на направление {b[i]}: " + str(a['Экз'].values.item()))

    prohodnoy = ['проходной', 'поступить', 'порог поступить', 'поступление', 'минимальный']
    if question_from_user(sentence, prohodnoy):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(f"Минимальный проходной балл в прошлом году на направлении {b[i]}: " + str(
                a['Мингод'].values.item()) + ' балл(-ов).')

    zayavka = ['заявление', 'подать', 'подача', 'порог заявление']
    if question_from_user(sentence, zayavka):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(
                f"Минимальный балл на подачу заявление на поступление в прошлом году на направлении {b[i]}: " + str(
                    a['Мин'].values.item()) + ' балл(-ов).')

    budget = ['бюджет', 'бюджетный', 'бюджетник', 'бюджетным']
    if question_from_user(sentence, budget):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(f"Количество бюджетных мест на направлении {b[i]}: " + str(a['Бюдж'].values.item()))

    tcelevoy = ['целевой', 'целевых', 'целевик', 'целевым']
    if question_from_user(sentence, tcelevoy):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(
                f"Количество целевых мест на направлении {b[i]}: " + str(a['Целевик'].values.item()))

    kvota = ['квотный', 'квотных', 'квотник', 'квотным']
    if question_from_user(sentence, kvota):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(f"Количество квотных мест на направлении {b[i]}: " + str(a['Квота'].values.item()))

    platn = ['платный', 'платник', 'платных', 'платным']
    if question_from_user(sentence, platn):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(f"Количество платных мест на направлении {b[i]}: " + str(a['Плат'].values.item()))

    konk = ['конкурс', 'человек']
    if question_from_user(sentence, konk):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(f"Конкурс в 2022 году на направлении {b[i]}: " + str(a['Конкурс'].values.item()) + " человек на место")

    doc = ['документ']
    if question_from_user(sentence, doc):
       a = df3[df3['Название'] == b[1]]
       answers[user_id].append(str(a['Документы'].values.item()))

    mest = ['все']
    if question_from_user(sentence, mest):
        for i in range(len(b)):
            a = df3[df3['Название'] == b[i]]
            answers[user_id].append(f"Всего мест на направлении {b[i]}: " + str(a['МестОбщ'].values.item()))

    if not question_from_user(sentence, platn):
        if not question_from_user(sentence, kvota):
            if not question_from_user(sentence, tcelevoy):
                if not question_from_user(sentence, budget):
                    if not question_from_user(sentence, zayavka):
                        if not question_from_user(sentence, prohodnoy):
                            if not question_from_user(sentence, exam):
                                if not question_from_user(sentence, price):
                                    if not question_from_user(sentence, konk):
                                        if not question_from_user(sentence, doc):
                                            if not question_from_user(sentence, mest):
                                                answers[user_id].append(f"Повторите еще раз вопрос\nВозможные проблемы:\n-) Некорректно указан вопрос\n-) Неправильно введено направление")
    return answers


bot.infinity_polling()
