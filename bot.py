import telebot
import pymysql
import os
import paramiko
import re
from telebot import types

#check atom git 
token ="337579434:AAEj1McwA85EnGo3Azygg7Y5UZpeILn9v1g"
bot = telebot.TeleBot(token)

allowed_users = ['191857882','285977295']
#check auth
def allow_user(chatid):
    strid = str(chatid)
    for item in allowed_users:
        if item == strid:
            return True
    return False
#Cameras
@bot.message_handler(commands=['start'])

def start(m):
    if allow_user(m.chat.id):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name , callback_data=name) for name in ['Включить наблюдение','Выключить наблюдение','Статус','Рестарт','Выключить сервер','Основной инет - Ростелеком','Основной инет - Мегафон']])
        msg = bot.send_message(m.chat.id, 'Что сделать?' , reply_markup=keyboard,parse_mode='Markdown')

    else:
        msg = bot.send_message(m.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(m.chat.id))
@bot.callback_query_handler(func=lambda c: True)
def inline(c):
	if c.data == 'Включить наблюдение':
		bot.answer_callback_query(callback_query_id=c.id,show_alert=True, text="Включено")
		bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id,text='*НАБЛЮДЕНИЕ ВКЛЮЧЕНО*',parse_mode='Markdown')
		db = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='kochergin1', db='zm' , port='3306')
		cursor = db.cursor()
		cursor.execute("UPDATE `Monitors` SET `Enabled` = 1")
		db.commit()
		db.close()
		os.system('service zoneminder restart')
	elif c.data == 'Выключить наблюдение':
		bot.answer_callback_query(callback_query_id=c.id,show_alert=True, text="Выключено")
		bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id,text='*НАБЛЮДЕНИЕ ВЫКЛЮЧЕНО*',parse_mode='Markdown')
		db = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='kochergin1', db='zm' , port='3306')
		cursor = db.cursor()
		cursor.execute("UPDATE `Monitors` SET `Enabled` = 0")
		db.commit()
		db.close()
		os.system('service zoneminder restart')
	elif c.data == 'Статус':
		db = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='kochergin1', db='zm' , port='3306')
		cursor = db.cursor()
		cursor.execute("SELECT `Enabled` FROM `Monitors` WHERE `Name` = 'Dvor'")
		for row in cursor.fetchall():
			if row[0] == 1:
				bot.answer_callback_query(callback_query_id=c.id,show_alert=True, text="Наблюдение включено")
				#bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id,text='*Статус:Наблюдение включено*',parse_mode='Markdown')
			else:
				bot.answer_callback_query(callback_query_id=c.id,show_alert=True, text="Наблюдение выключено")
				#bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id,text='*Статус:Наблюдение выключено*',parse_mode='Markdown')
		db.commit()
		db.close()
	elif c.data == 'Рестарт':
		os.system('service zoneminder restart')
		bot.answer_callback_query(callback_query_id=c.id,show_alert=True, text="Рестарт выполнен")
	elif c.data == 'Выключить сервер':
		os.system('shutdown -h +1')
		bot.answer_callback_query(callback_query_id=c.id,show_alert=True, text="Сервер выключен")
	elif c.data == 'Основной инет - Ростелеком':
		bot.answer_callback_query(callback_query_id=c.id,show_alert=True, text="Включен Ростелеком")
		bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id,text='*Ростелеком Основной*',parse_mode='Markdown')
		host = '192.168.1.1'
		user = 'admin'
		secret = 'kochergin1'
		port = 22
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname=host, username=user, password=secret, port=port)
		stdin, stdout, stderr = client.exec_command('ip route set [find comment="MEGAFON"] distance=4')
		data = stdout.read() + stderr.read()
		client.close()
	elif c.data == 'Основной инет - Мегафон':
		bot.answer_callback_query(callback_query_id=c.id,show_alert=True, text="Включен Мегафон")
		bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id,text='*Мегафон Основной*',parse_mode='Markdown')
		host = '192.168.1.1'
		user = 'admin'
		secret = 'kochergin1'
		port = 22
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname=host, username=user, password=secret, port=port)
		stdin, stdout, stderr = client.exec_command('ip route set [find comment="MEGAFON"] distance=2')
		data = stdout.read() + stderr.read()
		client.close()
bot.polling()
