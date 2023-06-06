import paramiko
import time
import shutil

host = '192.168.50.41'
user = 'pi'
secret = 'pi'
port = 22


shutil.make_archive("inf_bot", 'zip', "jjj")
client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(hostname=host, username=user, password=secret, look_for_keys=False, allow_agent=False)

ssh = client.invoke_shell()

ssh.send("sudo systemctl stop bot")
time.sleep(1)
client.exec_command('rm -rf inf_bot')
time.sleep(10)


sftp = client.open_sftp()
sftp.put("inf_bot.zip", "/home/pi/inf_bot.zip")
time.sleep(10)

sftp.close()
client.exec_command('unzip inf_bot.zip')
time.sleep(2)
client.exec_command('rm inf_bot.zip')
time.sleep(2)
ssh.send("sudo systemctl start bot")
time.sleep(2)

ssh.close()

print("Well done!")