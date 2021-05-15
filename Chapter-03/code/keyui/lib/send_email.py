import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from email.mime.text import MIMEText

from .log_config import get_logger
from .read_config import readConfig
_mylogger = get_logger('send_mail')

mailto_list = readConfig('config.ini','email','mailto_list').replace(' ','').split(',') # 收件人列表
mail_host = readConfig('config.ini','email','mail_host') # 配置邮件服务器
mail_from = readConfig('config.ini','email','mail_from') #发件人
mail_pass = readConfig('config.ini','email','mail_pass') #密码


def send_mail( sub, content, reportFile ):          # to_list：收件人；sub：主题；content：邮件内容
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    part = MIMEApplication(open(reportFile, 'rb').read())
    part.add_header('Content-Disposition', 'attachment',filename=Header(os.path.basename(reportFile),"utf-8").encode())
    #part["Content-Disposition"] = 'attachment; filename="%s"'%reportFile
    msg.attach(part) #添加附件

    msg['subject'] = Header(sub, 'utf-8').encode()
    msg['From'] = mail_from
    msg['To'] = ','.join(mailto_list) #兼容多个收件人
    smtp = smtplib.SMTP()

    try:
        smtp.connect(mail_host)
        smtp.login(mail_from, mail_pass)
        smtp.sendmail(mail_from, mailto_list, msg.as_string())
        smtp.close()
        _mylogger.info('带附件测试报告发送成功！')
        return True
    except (Exception) as e:
        _mylogger.error('邮件发送失败：%s' %e)
        return False
if __name__ == '__main__':
    content= "测试"
    #reportFile = 'log_config.py'
    reportFile='d:/居住证信息采集表.xls'
    email_result = send_mail("自动化测试结果",content, reportFile)
    if email_result:
        print ("发送成功")
    else:
        _mylogger.error(email_result)
        print ("发送失败")