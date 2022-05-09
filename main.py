import telebot
import pandas as pd
from pymystem3 import Mystem

document_text = open('info.csv', 'r')
text_string = document_text.read().lower()
df = pd.read_csv('info.csv', delimiter=';', encoding='1251')
bot = telebot.TeleBot('1694618937:AAF1ZWyYK5fuHcUIZx8CGRCyGtDEsBlPxqY')
keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).row('Места', 'Прочее')


button1 = 'Количество бюджетных мест'
button2 = 'Количество целевых мест'
button3 = 'Количество квотных мест'
button4 = 'Количество платных мест'
button5 = 'Назад'
keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).add(button3).add(
    button4).add(button5)

button6 = 'Цена за обучение'
button7 = 'Какие экзамены нужно сдавать?'
button8 = 'Минимальные проходные баллы'
button9 = 'Минимальные баллы в прошлом году'
keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button6).add(button7).add(button8).add(
    button9).add(button5)
keyboard4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard4.row('Поиск по коду', 'Поиск по названию', 'Назад')
keyboard5 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard5.row('Назад')
choice = 0


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id,
                     f'Я бот для абитуриентов ПетрГУ. Приятно познакомиться, {message.from_user.first_name}',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global choice
    if message.text == 'Места':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)
    if message.text == 'Прочее':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard3)
    if message.text == 'Количество бюджетных мест':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        choice = 1
        bot.register_next_step_handler(message, get_var_budget)
    if message.text == 'Количество целевых мест':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        choice = 2
        bot.register_next_step_handler(message, get_var_target)
    if message.text == 'Количество платных мест':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        choice = 3
        bot.register_next_step_handler(message, get_var_paid)
    if message.text == 'Количество квотных мест':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        choice = 4
        bot.register_next_step_handler(message, get_var_q)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard1)
    if message.text == 'Цена за обучение':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        choice = 5
        bot.register_next_step_handler(message, get_var_cost)
    if message.text == 'Какие экзамены нужно сдавать?':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        choice = 6
        bot.register_next_step_handler(message, get_var_exam)
    if message.text == 'Минимальные проходные баллы':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        choice = 7
        bot.register_next_step_handler(message, get_var_proh)
    if message.text == 'Минимальные баллы в прошлом году':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        choice = 8
        bot.register_next_step_handler(message, get_var_min)


def get_var_budget(message):
    if message.text == 'Поиск по коду':
        bot.send_message(message.from_user.id, 'Введите номер направления без точек и пробелов', reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_code_budget)
    if message.text == 'Поиск по названию':
        bot.send_message(message.from_user.id, 'Введите название направления', reply_markup=keyboard5)
        bot.register_next_step_handler(message, name)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)


def get_code_budget(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_budget)
        return
    global code
    code = message.text
    if is_number(code):
        a = df[df['Код'] == float(code)]
        if len(a) > 1:
            bot.send_message(message.from_user.id, 'В введенном номере несколько направлений, выберите другое меню',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_budget)
            return
        if len(a) == 0:
            bot.send_message(message.from_user.id, 'Не найдено направления с таким кодом',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_budget)
            return
        bot.send_message(message.from_user.id,
                         'Количество бюджетных мест на направлении ' + str(a['Название'].values.item()) + ': ' + str(
                             a['Бюдж'].values.item()), reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_budget)
    else:
        bot.send_message(message.from_user.id,'Введите число')
        bot.register_next_step_handler(message, get_code_budget)


def get_var_target(message):
    if message.text == 'Поиск по коду':
        bot.send_message(message.from_user.id, 'Введите номер направления без точек и пробелов', reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_code_target)
    if message.text == 'Поиск по названию':
        bot.send_message(message.from_user.id, 'Введите название направления', reply_markup=keyboard5)
        bot.register_next_step_handler(message, name)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)


def get_code_target(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_target)
        return
    global code
    code = message.text
    if is_number(code):
        a = df[df['Код'] == float(code)]
        if len(a) > 1:
            bot.send_message(message.from_user.id, 'В введенном номере несколько направлений, выберите другое меню',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_target)
            return
        bot.send_message(message.from_user.id,
                         'Количество целевых мест на направлении ' + str(a['Название'].values.item()) + ': ' + str(
                             a['Целевик'].values.item()), reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_target)
    else:
        bot.send_message(message.from_user.id,'Введите число')
        bot.register_next_step_handler(message, get_code_target)


def get_var_paid(message):
    if message.text == 'Поиск по коду':
        bot.send_message(message.from_user.id, 'Введите номер направления без точек и пробелов', reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_code_paid)
    if message.text == 'Поиск по названию':
        bot.send_message(message.from_user.id, 'Введите название направления', reply_markup=keyboard5)
        bot.register_next_step_handler(message, name)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)


def get_code_paid(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_paid)
        return
    global code
    code = message.text
    if is_number(code):
        a = df[df['Код'] == float(code)]
        if len(a) > 1:
            bot.send_message(message.from_user.id, 'В введенном номере несколько направлений, выберите другое меню',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_paid)
            return
        bot.send_message(message.from_user.id,
                         'Количество платных мест на направлении ' + str(a['Название'].values.item()) + ': ' + str(
                             a['Плат'].values.item()), reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_paid)
    else:
        bot.send_message(message.from_user.id,'Введите число')
        bot.register_next_step_handler(message, get_code_paid)



def get_var_q(message):
    if message.text == 'Поиск по коду':
        bot.send_message(message.from_user.id, 'Введите номер направления без точек и пробелов', reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_code_q)
    if message.text == 'Поиск по названию':
        bot.send_message(message.from_user.id, 'Введите название направления', reply_markup=keyboard5)
        bot.register_next_step_handler(message, name)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)


def get_code_q(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_q)
        return
    global code
    code = message.text
    if is_number(code):
        a = df[df['Код'] == float(code)]
        if len(a) > 1:
            bot.send_message(message.from_user.id, 'В введенном номере несколько направлений, выберите другое меню',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_q)
            return
        bot.send_message(message.from_user.id,
                         'Количество квотных мест на направлении ' + str(a['Название'].values.item()) + ': ' + str(
                             a['Квота'].values.item()), reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_q)
    else:
        bot.send_message(message.from_user.id,'Введите число')
        bot.register_next_step_handler(message, get_code_q)


def get_var_cost(message):
    if message.text == 'Поиск по коду':
        bot.send_message(message.from_user.id, 'Введите номер направления без точек и пробелов', reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_code_cost)
    if message.text == 'Поиск по названию':
        bot.send_message(message.from_user.id, 'Введите название направления', reply_markup=keyboard5)
        bot.register_next_step_handler(message, name)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)


def get_code_cost(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_cost)
        return
    global code
    code = message.text
    if is_number(code):
        a = df[df['Код'] == float(code)]
        if len(a) > 1:
            bot.send_message(message.from_user.id, 'В введенном номере несколько направлений, выберите другое меню',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_cost)
            return
        bot.send_message(message.from_user.id,
                         'Цена за обучение на направлении ' + str(a['Название'].values.item()) + ': ' + str(
                             a['Цена'].values.item()), reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_cost)
    else:
        bot.send_message(message.from_user.id,'Введите число')
        bot.register_next_step_handler(message, get_code_cost)

def get_var_exam(message):
    if message.text == 'Поиск по коду':
        bot.send_message(message.from_user.id, 'Введите номер направления без точек и пробелов', reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_code_exam)
    if message.text == 'Поиск по названию':
        bot.send_message(message.from_user.id, 'Введите название направления', reply_markup=keyboard5)
        bot.register_next_step_handler(message, name)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)


def get_code_exam(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_exam)
        return
    global code
    code = message.text
    if is_number(code):
        a = df[df['Код'] == float(code)]
        if len(a) > 1:
            bot.send_message(message.from_user.id, 'В введенном номере несколько направлений, выберите другое меню',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_exam)
            return
        bot.send_message(message.from_user.id,
                         'Экзамены, которые нужно сдавать на направлении ' + str(a['Название'].values.item()) + ': ' + str(
                             a['Экз'].values.item()), reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_exam)
    else:
        bot.send_message(message.from_user.id,'Введите число')
        bot.register_next_step_handler(message, get_code_exam)


def get_var_proh(message):
    if message.text == 'Поиск по коду':
        bot.send_message(message.from_user.id, 'Введите номер направления без точек и пробелов', reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_code_proh)
    if message.text == 'Поиск по названию':
        bot.send_message(message.from_user.id, 'Введите название направления', reply_markup=keyboard5)
        bot.register_next_step_handler(message, name)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)


def get_code_proh(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_proh)
        return
    global code
    code = message.text
    if is_number(code):
        a = df[df['Код'] == float(code)]
        if len(a) > 1:
            bot.send_message(message.from_user.id, 'В введенном номере несколько направлений, выберите другое меню',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_proh)
            return
        bot.send_message(message.from_user.id,
                         'Минимальные проходные баллы на направлении ' + str(a['Название'].values.item()) + ': ' + str(
                             a['Мин'].values.item()), reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_proh)
    else:
        bot.send_message(message.from_user.id,'Введите число')
        bot.register_next_step_handler(message, get_code_proh)


def get_var_min(message):
    if message.text == 'Поиск по коду':
        bot.send_message(message.from_user.id, 'Введите номер направления без точек и пробелов', reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_code_min)
    if message.text == 'Поиск по названию':
        bot.send_message(message.from_user.id, 'Введите название направления', reply_markup=keyboard5)
        bot.register_next_step_handler(message, name)
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard2)


def get_code_min(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_min)
        return
    global code
    code = message.text
    if is_number(code):
        a = df[df['Код'] == float(code)]
        if len(a) > 1:
            bot.send_message(message.from_user.id, 'В введенном номере несколько направлений, выберите другое меню',
                             reply_markup=keyboard4)
            bot.register_next_step_handler(message, get_var_min)
            return
        bot.send_message(message.from_user.id,
                         'Минимальные баллы в прошлом году на направлении ' + str(a['Название'].values.item()) + ': ' + str(
                             a['Мингод'].values.item()), reply_markup=keyboard4)
        bot.register_next_step_handler(message, get_var_min)
    else:
        bot.send_message(message.from_user.id,'Введите число')
        bot.register_next_step_handler(message, get_code_min)

def name(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите интересующее вас меню', reply_markup=keyboard1)
        bot.register_next_step_handler(message, get_text_messages)
    document_text = message.text
    text_string = document_text.lower()
    df3 = pd.read_csv('info.csv', delimiter=';', encoding='1251')
    df = pd.read_csv('new.csv', delimiter=';', encoding='1251')
    df2 = pd.read_csv('info_short.csv', delimiter=';', encoding='1251')
    D = {}
    a = text_string.split(';')
    m = Mystem()
    n = len(a)
    j = 0

    for s in a:
        lemmas = m.lemmatize(s)
        for lemma in lemmas:
            if lemma.isalpha():
                l = D.get(lemma, [0] * n)
                l[j] = l[j] + 1
                D[lemma] = l
        j = j + 1
#383-419 определение того какое направление написал пользователь
    b = []
    for i in D.keys():
        a = df[df['name'] == i]
        new_list = [item for sublist in a.values.tolist() for item in sublist]
        b.append(new_list)
        if len(new_list) == 0:
            bot.send_message(message.from_user.id, 'Направление не найдено', reply_markup=keyboard1)
            b.clear()
            D.clear()
            bot.register_next_step_handler(message, get_text_messages)
            return
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





    if choice == 1:
        for i in final_dict.keys():
            i = int(i)
            a = df3[df3['Название'] == df2.columns[i]]
            bot.send_message(message.from_user.id,f'Количество бюджетных мест на направлении {df2.columns[i]}: ' + str(a['Бюдж'].values.item()))
    if choice == 2:
        for i in final_dict.keys():
            i = int(i)
            a = df3[df3['Название'] == df2.columns[i]]
            bot.send_message(message.from_user.id,f'Количество целевых мест на направлении {df2.columns[i]}: ' + str(a['Целевик'].values.item()))
    if choice == 3:
        for i in final_dict.keys():
            i = int(i)
            a = df3[df3['Название'] == df2.columns[i]]
            bot.send_message(message.from_user.id,f'Количество платных мест на направлении {df2.columns[i]}: ' + str(a['Плат'].values.item()))
    if choice == 4:
        for i in final_dict.keys():
            i = int(i)
            a = df3[df3['Название'] == df2.columns[i]]
            bot.send_message(message.from_user.id,f'Количество квотных мест на направлении {df2.columns[i]}: ' + str(a['Квота'].values.item()))
    if choice == 5:
        for i in final_dict.keys():
            i = int(i)
            a = df3[df3['Название'] == df2.columns[i]]
            bot.send_message(message.from_user.id,f'Цена за обучение на направлении {df2.columns[i]}: ' + str(a['Цена'].values.item()))
    if choice == 6:
        for i in final_dict.keys():
            i = int(i)
            a = df3[df3['Название'] == df2.columns[i]]
            bot.send_message(message.from_user.id,f'Экзамены, которые нужны на направлении {df2.columns[i]}: ' + str(a['Экз'].values.item()))
    if choice == 7:
        for i in final_dict.keys():
            i = int(i)
            a = df3[df3['Название'] == df2.columns[i]]
            bot.send_message(message.from_user.id,f'Минимальные проходные баллы на направлении {df2.columns[i]}: ' +str(a['Мин'].values.item()))
    if choice == 8:
        for i in final_dict.keys():
            i = int(i)
            a = df3[df3['Название'] == df2.columns[i]]
            bot.send_message(message.from_user.id, f'Минимальные проходные баллы в прошлом году на направлении {df2.columns[i]} : '+ str(a['Мингод'].values.item()))


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


bot.polling(none_stop=True)
