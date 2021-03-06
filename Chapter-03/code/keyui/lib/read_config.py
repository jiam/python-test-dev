import configparser
import os

def readConfig(file,field,key):
    '''

    :param file:
    :param field:
    :param key:
    :return:
    '''
    config = configparser.ConfigParser()
    conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","config",file))
    config.read_file(open(conf_path, "r", encoding='UTF-8'))

    return config.get(field, key)

if __name__ =='__main__':
    mail_host= readConfig('config.ini','email','mail_host')
    print(mail_host)