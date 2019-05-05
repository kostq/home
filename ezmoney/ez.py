import telebot
import pymysql
import os
import paramiko
import re
from telebot import types
from telebot import apihelper
import time
import db_con
import ez_config


API_TOKEN = ez_config.token

bot = telebot.TeleBot(API_TOKEN)
user_dict = {}

allowed_users = [ez_config.user1]

apihelper.proxy = {'https': 'socks5://{}:{}@{}:{}'.format(
    ez_config.proxy_login, ez_config.proxy_pass, ez_config.proxy_ip, ez_config.proxy_port)}


class User:
    def __init__(self, main_cat):
        self.main_cat = main_cat
        self.category = None
        self.summ = None
        self.source = None
        self.notes = None


# check auth
def allow_user(chatid):
    strid = str(chatid)
    for item in allowed_users:
        if item == strid:
            return True
    return False

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if allow_user(message.chat.id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Расход', 'Приход', 'Перевод')
        msg = bot.reply_to(message, 'Выбери действие', reply_markup=markup)
        bot.register_next_step_handler(msg, choose_category)
    else:
        msg = bot.reply_to(
            message, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))


def choose_category(message):

    main_cat = message.text
    chat_id = message.chat.id
    user = User(main_cat)
    user_dict[chat_id] = user
    if (main_cat == u'Расход'):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('ЖКХ', 'Продукты', 'Сотовая связь', 'Интернет', 'Проезд', 'Одежда', 'Обучение',
                   'Техника', 'Парикмахерская', 'Подарки и ДР', 'Медикаменты', 'Развлечения и отдых', 'Прочее')
        msg = bot.reply_to(message, 'Выбери категорию', reply_markup=markup)
        bot.register_next_step_handler(msg, take_sum)
    elif (main_cat == u'Приход'):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Зарплата', 'Шабашка', 'Возврат долга', 'Прочее')
        msg = bot.reply_to(message, 'Выбери категорию', reply_markup=markup)
        bot.register_next_step_handler(msg, take_sum)
    elif (main_cat == u'Перевод'):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Карта 4048', 'Карта 3580', 'Карта tinkoff',
                   'Наличные', 'Сбер счет 2601')
        msg = bot.reply_to(message, 'ОТКУДА', reply_markup=markup)
        bot.register_next_step_handler(msg, change_a)


def change_a(message):
    chat_id = message.chat.id
    change_source_a = message.text  # счет ОТКУДА
    user = user_dict[chat_id]
    user.change_source_a = change_source_a
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Карта 4048', 'Карта 3580', 'Карта tinkoff',
               'Наличные', 'Сбер счет 2601')
    msg = bot.reply_to(message, 'КУДА', reply_markup=markup)
    bot.register_next_step_handler(msg, change_sum)


def change_sum(message):
    chat_id = message.chat.id
    change_source_b = message.text  # cчет КУДА
    user = user_dict[chat_id]
    user.change_source_b = change_source_b
    msg = bot.reply_to(message, 'Введите сумму')
    bot.register_next_step_handler(msg, change_check_sum)


def change_check_sum(message):
    chat_id = message.chat.id
    change_summ = message.text
    user = user_dict[chat_id]
    if not change_summ.isdigit():
        msg = bot.reply_to(message, 'Ты что-то напутал , введи сумму')
        bot.register_next_step_handler(msg, change_check_sum)
        return
    user.change_summ = change_summ
    msg = bot.reply_to(message, 'Введите комментарий')
    bot.register_next_step_handler(msg, change_action)


def take_sum(message):
    chat_id = message.chat.id
    category = message.text
    user = user_dict[chat_id]
    user.category = category
    msg = bot.reply_to(message, 'Введите сумму')
    bot.register_next_step_handler(msg, check_sum)


def check_sum(message):
    chat_id = message.chat.id
    summ = message.text
    if not summ.isdigit():
        msg = bot.reply_to(message, 'Ты что-то напутал , введи сумму')
        bot.register_next_step_handler(msg, check_sum)
        return
    user = user_dict[chat_id]
    user.summ = summ
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Карта 4048', 'Карта 3580', 'Карта tinkoff', 'Наличные')
    msg = bot.reply_to(message, 'Выбери счет', reply_markup=markup)
    bot.register_next_step_handler(msg, notes_and_go)


def notes_and_go(message):
    chat_id = message.chat.id
    source = message.text
    user = user_dict[chat_id]
    user.source = source
    msg = bot.reply_to(message, 'Введите комментарий')
    bot.register_next_step_handler(msg, action)


def action(message):
    chat_id = message.chat.id
    notes = message.text
    user = user_dict[chat_id]
    user.notes = notes
    connection = db_con.getConnection()
    try:
        with connection.cursor() as cursor:
            if user.main_cat == 'Расход':
                sql_ins = "INSERT INTO `spent_Money` (`category_id`,`source_id`,`sum`,`notes`) SELECT a.id, b.id, %s, %s FROM category AS a , source AS b WHERE a.name = %s AND b.name = %s"
                sql_upd = "UPDATE `source` SET `source_money` = `source_money` - %s WHERE `name` = %s"
                cursor.execute(sql_ins, (user.summ, user.notes,
                                         user.category, user.source))
                cursor.execute(sql_upd, (user.summ, user.source))
            elif user.main_cat == 'Приход':
                sql_ins = "INSERT INTO `recieve_Money` (`category_id`,`source_id`,`sum`,`notes`) SELECT a.id, b.id, %s, %s FROM category_recieve AS a , source AS b WHERE a.name = %s AND b.name = %s"
                sql_upd = "UPDATE `source` SET `source_money` = `source_money` + %s WHERE `name` = %s"
                cursor.execute(sql_ins, (user.summ, user.notes,
                                         user.category, user.source))
                cursor.execute(sql_upd, (user.summ, user.source))
            elif user.main_cat == 'Перевод':
                sql_upd_1 = "UPDATE `source` SET `source_money` = `source_money` + %s WHERE `name` = %s"
                sql_upd_2 = "UPDATE `source` SET `source_money` = `source_money` - %s WHERE `name` = %s"
                cursor.execute(
                    sql_upd_1, (user.change_summ, user.change_source_b))
                cursor.execute(
                    sql_upd_2, (user.change_summ, user.change_source_a))
            sql_sel = "SELECT `name`,`source_money` FROM `source`"
            cursor.execute(sql_sel)
            src4048 = cursor.fetchone()
            src4048_name = src4048["name"]
            src4048_money = src4048["source_money"]
            src3580 = cursor.fetchone()
            src3580_name = src3580["name"]
            src3580_money = src3580["source_money"]
            srctinkoff = cursor.fetchone()
            srctinkoff_name = srctinkoff["name"]
            srctinkoff_money = srctinkoff["source_money"]
            srccash = cursor.fetchone()
            srccash_name = srccash["name"]
            srccash_money = srccash["source_money"]
    finally:
        connection.commit()
    bot.send_message(chat_id, '‼️‼️‼️' + user.main_cat + '‼️‼️‼️' + '\n🛒Категория: ' + user.category +
                     '\n💰Сумма: ' + user.summ + ' руб' + '\n💳Счет: ' + user.source + '\n📝Комментарий: ' + user.notes)
    bot.send_message(chat_id, 'Остаток по счетам\n' + src4048_name + ' - ' + str(int(src4048_money)) + ' руб\n' + src3580_name + ' - ' + str(int(src3580_money)
                                                                                                                                             ) + ' руб\n' + srctinkoff_name + ' - ' + str(int(srctinkoff_money)) + ' руб\n' + srccash_name + ' - ' + str(int(srccash_money)) + ' руб\n')


def change_action(message):
    chat_id = message.chat.id
    notes = message.text
    user = user_dict[chat_id]
    user.change_notes_spent = 'Перевод с счета ' + user.change_source_a
    user.change_notes_recieve = 'Перевод на счет ' + user.change_source_b
    user.change_category = 'Перевод между счетами'
    connection = db_con.getConnection()
    try:
        with connection.cursor() as cursor:
            if user.main_cat == 'Перевод':
                sql_ins_spent = "INSERT INTO `spent_Money` (`category_id`,`source_id`,`sum`,`notes`) SELECT a.id, b.id, %s, %s FROM category AS a , source AS b WHERE a.name = %s AND b.name = %s"
                sql_ins_recieve = "INSERT INTO `recieve_Money` (`category_id`,`source_id`,`sum`,`notes`) SELECT a.id, b.id, %s, %s FROM category_recieve AS a , source AS b WHERE a.name = %s AND b.name = %s"
                sql_upd_1 = "UPDATE `source` SET `source_money` = `source_money` + %s WHERE `name` = %s"
                sql_upd_2 = "UPDATE `source` SET `source_money` = `source_money` - %s WHERE `name` = %s"
                cursor.execute(sql_ins_spent, (user.change_summ, user.change_notes_spent,
                                               user.change_category, user.change_source_a))
                cursor.execute(sql_ins_recieve, (user.change_summ,
                                                 user.change_notes_recieve, user.change_category, user.change_source_b))
                cursor.execute(
                    sql_upd_1, (user.change_summ, user.change_source_b))
                cursor.execute(
                    sql_upd_2, (user.change_summ, user.change_source_a))
            sql_sel = "SELECT `name`,`source_money` FROM `source`"
            cursor.execute(sql_sel)
            src4048 = cursor.fetchone()
            src4048_name = src4048["name"]
            src4048_money = src4048["source_money"]
            src3580 = cursor.fetchone()
            src3580_name = src3580["name"]
            src3580_money = src3580["source_money"]
            srctinkoff = cursor.fetchone()
            srctinkoff_name = srctinkoff["name"]
            srctinkoff_money = srctinkoff["source_money"]
            srccash = cursor.fetchone()
            srccash_name = srccash["name"]
            srccash_money = srccash["source_money"]
    finally:
        connection.commit()
    bot.send_message(chat_id, '‼️‼️‼️' + 'Было переведено ' + user.change_summ + ' руб' +
                     ' с счета ' + user.change_source_a + ' на счет ' + user.change_source_b + '‼️‼️‼️')
    bot.send_message(chat_id, 'Остаток по счетам\n' + src4048_name + ' - ' + str(int(src4048_money)) + ' руб\n' + src3580_name + ' - ' + str(int(src3580_money)
                                                                                                                                             ) + ' руб\n' + srctinkoff_name + ' - ' + str(int(srctinkoff_money)) + ' руб\n' + srccash_name + ' - ' + str(int(srccash_money)) + ' руб\n')


@bot.message_handler(commands=['stats'])
def stats(message):
    if allow_user(message.chat.id):
        chat_id = message.chat.id
        connection = db_con.getConnection()
        try:
            with connection.cursor() as cursor:
                sql_sel = "SELECT `name`,`source_money` FROM `source`"
                cursor.execute(sql_sel)
                src4048 = cursor.fetchone()
                src4048_name = src4048["name"]
                src4048_money = src4048["source_money"]
                src3580 = cursor.fetchone()
                src3580_name = src3580["name"]
                src3580_money = src3580["source_money"]
                srctinkoff = cursor.fetchone()
                srctinkoff_name = srctinkoff["name"]
                srctinkoff_money = srctinkoff["source_money"]
                srccash = cursor.fetchone()
                srccash_name = srccash["name"]
                srccash_money = srccash["source_money"]
                srcsber1 = cursor.fetchone()
                srcsber1_name = srcsber1["name"]
                srcsber1_money = srcsber1["source_money"]
                src_all = src4048_money + src3580_money + \
                    srctinkoff_money + srccash_money + srcsber1_money
        finally:
            bot.send_message(chat_id, 'Остаток по счетам\n' + src4048_name + ' - ' + str(int(src4048_money)) + ' руб\n' + src3580_name + ' - ' + str(int(src3580_money)) + ' руб\n' + srctinkoff_name + ' - ' + str(
                int(srctinkoff_money)) + ' руб\n' + srccash_name + ' - ' + str(int(srccash_money)) + ' руб\n' + srcsber1_name + ' - ' + str(int(srcsber1_money)) + ' руб\n' + '\nИтого: ' + str(int(src_all)) + ' руб\n')
    else:
        msg = bot.reply_to(
            message, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))


bot.polling()
