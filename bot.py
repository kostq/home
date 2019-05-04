import telebot
import pymysql
import os
import paramiko
import re
import botconfig as con
import requests
from telebot import types
from telebot import apihelper

token = con.token
bot = telebot.TeleBot(token)
apihelper.proxy = {'https':'socks5://rkn_must_die:noutek_4ever@195.2.253.155:7081'}

# router config
host = con.routerip
user = con.routeruser
secret = con.routerpass
port = 22

allowed_users = [con.user1, con.user2]
# check auth


def allow_user(chatid):
    strid = str(chatid)
    for item in allowed_users:
        if item == strid:
            return True
    return False


@bot.message_handler(commands=['start'])
def start(m):
    if allow_user(m.chat.id):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Включить наблюдение',
                                                                                              'Выключить наблюдение', 'Статус', 'Рестарт', 'Выключить сервер', 'Основной инет - Ростелеком', 'Основной инет - Мегафон']])
        msg = bot.send_message(m.chat.id, 'Что сделать?',
                               reply_markup=keyboard, parse_mode='Markdown')

    else:
        msg = bot.send_message(
            m.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(m.chat.id))


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'Включить наблюдение':
        bot.answer_callback_query(
            callback_query_id=c.id, show_alert=True, text="Включено")
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                              text='*НАБЛЮДЕНИЕ ВКЛЮЧЕНО*', parse_mode='Markdown')
        db = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock',
                             user=con.mysqluser, passwd=con.mysqlpass, db=con.mysqldb, port='3306')
        cursor = db.cursor()
        cursor.execute("UPDATE `Monitors` SET `Enabled` = 1")
        db.commit()
        db.close()
        os.system('service zoneminder restart')
    elif c.data == 'Выключить наблюдение':
        bot.answer_callback_query(
            callback_query_id=c.id, show_alert=True, text="Выключено")
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                              text='*НАБЛЮДЕНИЕ ВЫКЛЮЧЕНО*', parse_mode='Markdown')
        db = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock',
                             user=con.mysqluser, passwd=con.mysqlpass, db=con.mysqldb, port='3306')
        cursor = db.cursor()
        cursor.execute("UPDATE `Monitors` SET `Enabled` = 0")
        db.commit()
        db.close()
        os.system('service zoneminder restart')
    elif c.data == 'Статус':
        db = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock',
                             user=con.mysqluser, passwd=con.mysqlpass, db=con.mysqldb, port='3306')
        cursor = db.cursor()
        cursor.execute(
            "SELECT `Enabled` FROM `Monitors` WHERE `Name` = 'Dvor'")
        for row in cursor.fetchall():
            if row[0] == 1:
                bot.answer_callback_query(
                    callback_query_id=c.id, show_alert=True, text="Наблюдение включено")
                #bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id,text='*Статус:Наблюдение включено*',parse_mode='Markdown')
            else:
                bot.answer_callback_query(
                    callback_query_id=c.id, show_alert=True, text="Наблюдение выключено")
                #bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id,text='*Статус:Наблюдение выключено*',parse_mode='Markdown')
        db.commit()
        db.close()
    elif c.data == 'Рестарт':
        os.system('service zoneminder restart')
        bot.answer_callback_query(
            callback_query_id=c.id, show_alert=True, text="Рестарт выполнен")
    elif c.data == 'Выключить сервер':
        os.system('shutdown -h +1')
        bot.answer_callback_query(
            callback_query_id=c.id, show_alert=True, text="Сервер выключен")
    elif c.data == 'Основной инет - Ростелеком':
        bot.answer_callback_query(
            callback_query_id=c.id, show_alert=True, text="Включен Ростелеком")
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                              text='*Ростелеком Основной*', parse_mode='Markdown')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user,
                       password=secret, port=port)
        stdin, stdout, stderr = client.exec_command(
            'ip route set [find comment="MEGAFON"] distance=4')
        data = stdout.read() + stderr.read()
        client.close()
    elif c.data == 'Основной инет - Мегафон':
        bot.answer_callback_query(
            callback_query_id=c.id, show_alert=True, text="Включен Мегафон")
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                              text='*Мегафон Основной*', parse_mode='Markdown')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user,
                       password=secret, port=port)
        stdin, stdout, stderr = client.exec_command(
            'ip route set [find comment="MEGAFON"] distance=2')
        data = stdout.read() + stderr.read()
        client.close()


bot.polling(none_stop=True, timeout = 50)
