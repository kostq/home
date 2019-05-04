import pymysql	

def getConnection():
	connection = pymysql.connect(
		host='localhost',
		user='root',
		password='kochergin1',
		db='easymoney',
		charset='utf8',
		cursorclass=pymysql.cursors.DictCursor)	
	return connection