import telebot
import pymysql
import os
import paramiko
import re
from telebot import types
import db_con


connection = db_con.getConnection()
try:
	with connection.cursor() as cursor:
		cursor.execute ("SELECT `name`,`source_money` FROM `source`")
		src7107 = cursor.fetchone()
		print (src7107["name"],'-',src7107["source_money"])
		src3580 = cursor.fetchone()
		print (src3580["name"],'-',src3580["source_money"])
		srctinkoff = cursor.fetchone()
		print (srctinkoff["name"],'-',srctinkoff["source_money"])
		srccash = cursor.fetchone()
		print (srccash["name"],'-',srccash["source_money"])
finally:
	connection.commit()
