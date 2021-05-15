import logging
import logging.handlers
from selenium import webdriver
import xlwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

rf_handler = logging.StreamHandler()
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler('job.log')
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)

def get_data():
    browser=webdriver.Chrome()
    url="https://movie.douban.com/"
    browser.get(url)
    el=browser.find_element_by_xpath('//*[@id="billboard"]/div[2]')
    data = el.text.split('\n')
    result = []
    for item in data:
        t = item.split(" ")
        sn = t[0]
        name = t[1]
        result.append((sn,name))
    return result

def write_excel(data):
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("豆瓣电影一周口碑榜")
    header = ["排位","名称"]
    for i in range(2):
        sheet.write(0,i,header[i])
    row = 1
    for item in data:
        for col in range(2):
            sheet.write(row,col,item[col])
        row += 1
    workbook.save('data.xls')

def send_mail():
    mail_host = 'smtp.qq.com'
    mail_user = '260137162@qq.com'
    mail_pass = 'dqoomkmjfovbbhga'   
    sender = '260137162@qq.com'
    receivers = ['260137162@qq.com']
    
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = '豆瓣电影-一周口碑榜'
    content='豆瓣电影-一周口碑榜'
    part1 = MIMEText(content,'plain','utf-8')
    

    with open('data.xls','rb') as h:
        content2 = h.read()
    part2 = MIMEText(content2,'base64','utf-8')
    part2['Content-Type'] = 'application/octet-stream'
    part2['Content-Disposition'] = 'attachment;filename="data.xls"'
    
   
    message.attach(part1)
    message.attach(part2)
    
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        logger.info('success')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        logger.error('error',exc_info=True)

data = get_data()
write_excel(data)
send_mail()





