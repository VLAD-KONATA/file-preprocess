import pynvml
pynvml.nvmlInit()
import time
import os
#from send_email import send_msg

import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
def send_msg(target_email,msg):
  # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
  message = MIMEText(msg, 'plain', 'utf-8')
  message["From"]=Header("KONATA <2232010872@qq.com>")  #header格式： [nickname]+空格+<[xxxx@qq.com]>,不声明为UTF-8
  message["To"] = Header("KONATA <2232010872@qq.com>")
  subject = 'nvidia显卡监控'
  message['Subject'] = Header(subject, 'utf-8')

  
  try:
      smtpObj = smtplib.SMTP()
      smtpObj.connect("smtp.qq.com")   # 连接 qq 邮箱
      smtpObj.login("2232010872@qq.com", "wrohdwqslavudjej")   # 账号和授权码
      smtpObj.sendmail("2232010872@qq.com", ["mfyang2000@qq.com"], message.as_string())   # 发送账号、接收账号和邮件信息
      print("邮件发送成功")
  except smtplib.SMTPException:
      print("Error: 无法发送邮件")


def watch_nvidia(nvidia_ids,min_memory):
  flag = [1 for i in nvidia_ids]
  for i in nvidia_ids:
    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    print("card {} free memory is {}GB".format(i,meminfo.free * 1.0 /(1024**3)))
    if meminfo.free * 1.0 /(1024**3) > min_memory:
      flag[i-1]=0
    else:
      flag[i-1]=1
  if 0 in flag:
    free_num = 0
    for i in flag:
      if i == 0:
        free_num += 1
    return free_num
  else:
    print("no free card!")
    return -1



nvidia_ids = [0] # 显卡id
min_memory = 20 # 最小可用显存 GB
while True:
  flag = watch_nvidia(nvidia_ids,min_memory)
  if flag >= 2:
    send_msg("mfyang2000@qq.com","{}张显卡空闲,自动启动训练".format(flag))
    #os.system("sh veri.sh") # your command
    break
  time.sleep(10)
    
#nohup python3 -u watch_nvidia.py > tmp.txt 2>&1 &


    



