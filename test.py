import paramiko 
import re

host = '192.168.1.1'
user = 'admin'
secret = 'kochergin1'
port = 55896
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Подключение
client.connect(hostname=host, username=user, password=secret, port=port)
 
# Выполнение команды
stdin, stdout, stderr = client.exec_command('ip route print where comment="MEGAFON"')
data = stdout.read() + stderr.read()
data = str(data)
result = re.search(r'A S',data)
if result:
	if result.group() == 'A S':
		res = 1
else:
	res = 0
print(res)
#print (data)
client.close()
