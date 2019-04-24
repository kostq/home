import paramiko

 
host = '192.168.1.1'
user = 'admin'
secret = 'kochergin1'
port = 22
 
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Подключение
client.connect(hostname=host, username=user, password=secret, port=port)
 
# Выполнение команды
stdin, stdout, stderr = client.exec_command('ip route set 1 distance 9')
 
# Читаем результат
data = stdout.read() + stderr.read()
print (data)
client.close()