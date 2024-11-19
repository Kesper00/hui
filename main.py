import telebot
import sqlite3

from telebot import types
import config
bot = telebot.TeleBot(config.TOKEN)

def insert_user(id,user):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"SELECT * FROM users WHERE id={id}"
    cur.execute(request)
    check = cur.fetchone()
    if check == None:
        request = f"INSERT INTO users(id,balance,user_id) VALUES({id},0,{user})"
        cur.execute(request)
        conn.commit()

def update_balance(id,sum):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"UPDATE users SET balance=balance+{sum} WHERE id={id}"
    cur.execute(request)
    conn.commit()

def get_balance(id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"SELECT balance FROM users WHERE id={id}"
    cur.execute(request)
    return cur.fetchone()

def get_referral_link(id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"SELECT ref_link FROM users WHERE id={id}"
    cur.execute(request)
    return cur.fetchone()

def check_referral(link):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"SELECT id FROM users WHERE ref_link={link}"
    cur.execute(request)
    return cur.fetchone()

def get_referrals(id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"SELECT referrals FROM users WHERE id={id}"
    cur.execute(request)
    return cur.fetchone()

def add_referral(id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"UPDATE users SET referrals=referrals+1 WHERE id={id}"
    cur.execute(request)
    conn.commit()


def update_ref_link(link,id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"UPDATE users SET ref_link='{link}' WHERE id={id}"
    cur.execute(request)
    conn.commit()


def get_all_users():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    request = f"SELECT user_id FROM users"
    cur.execute(request)
    return cur.fetchall()




@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    referrer = None

    # Проверяем наличие хоть какой-то дополнительной информации из ссылки
    if " " in message.text:
        referrer_candidate = message.text.split()[1]

        # Пробуем преобразовать строку в число
        try:
            referrer_candidate = int(referrer_candidate)

            # Проверяем на несоответствие TG ID пользователя TG ID реферера
            # Также проверяем, есть ли такой реферер в базе данных
            if user_id != referrer_candidate:
                referer = referrer_candidate
                add_referral(referer)
                print(referer)

        except ValueError:
            pass

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("☘️КЛИК☘")
    btn2 = types.KeyboardButton("💶БАЛАНС💶")
    btn3 = types.KeyboardButton("💵ВЫВОД💵")
    markup.add(btn1, btn2, btn3)
    starter = 'Поздравляем! Вы зашли в 💵Кликер РОБУКСОВ💵.'  # вместо кликер своё название группы
    insert_user(message.chat.id,message.from_user.id)
    bot.send_message(message.chat.id, starter, reply_markup=markup)
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "☘️КЛИК☘":
        bot.send_message(message.chat.id, text='Успешно\n+0.01 robux', reply_markup=None)
        update_balance(message.chat.id, 0.01)
    if message.text == "💶БАЛАНС💶":
        balance = get_balance(message.chat.id)[0]
        referrals = get_referrals(message.chat.id)[0]
        ref_link = get_referral_link(message.chat.id)[0].format(msg=message.from_user.id)
        update_ref_link(ref_link,message.chat.id)

        text = f"Ваш баланс: {balance:.2f} robux"
        text2 = f""
        if referrals >= 3:
            bot.send_message(message.chat.id, text, reply_markup=None)
        if referrals < 3:
            bot.send_message(message.chat.id, text=f'💰Для просмотра баланса и вывода денег вам необходимо:\n\nПригласить 3 человек в нашего бота, отправив им эту ссылку: {ref_link}\n🛑Ваши друзья должны обязательно выполнить те же условия, что и вы\n🛑По этой ссылке мы можем отслеживать количество людей, которых вы пригласили.\nПри выполнении наша поддержка сама напишет вам и выдаст баланс с выводом.', reply_markup=None)
    if message.text == "💵ВЫВОД💵":
        balance = get_balance(message.chat.id)[0]
        referrals = get_referrals(message.chat.id)[0]
        ref_link = get_referral_link(message.chat.id)[0].format(msg=message.from_user.id)
        text1 = f"Ваш вывод составляет: {balance:.2f}\nОбратитесь к @aqsw070"
        if referrals >= 3:
            bot.send_message(message.chat.id, text1, reply_markup=None)
        if referrals < 3:
            bot.send_message(message.chat.id, text=f'💰Для просмотра баланса и вывода денег вам необходимо:\n\nПригласить 3 человек в нашего бота, отправив им эту ссылку: {ref_link}\n🛑Ваши друзья должны обязательно выполнить те же условия, что и вы\n🛑По этой ссылке мы можем отслеживать количество людей, которых вы пригласили.\nПри выполнении наша поддержка сама напишет вам и выдаст баланс с выводом.', reply_markup=None)

bot.polling(none_stop=True)