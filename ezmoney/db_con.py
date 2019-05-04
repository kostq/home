import pymysql
import ez_config

def getConnection():
	connection = pymysql.connect(
		host='localhost',
		user=ez_config.mysqluser,
		password=ez_config.mysqlpass,
		db=ez_config.mysqldb,
		charset='utf8',
		cursorclass=pymysql.cursors.DictCursor)
	return connection
