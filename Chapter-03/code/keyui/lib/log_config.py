import logging
import os
from logging.handlers import RotatingFileHandler


'''
    CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
'''
    
def get_logger(name='root'):
    logpath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'log')
    log_file = os.path.join(logpath,'log.log')
    print(log_file)
    if not os.path.exists(logpath):
        os.makedirs(logpath)

 
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # 控制台、日志文件输出日志格式设置
    format1=logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(lineno)s %(message)s')
    format2=logging.Formatter('[%(name)s] [%(levelname)s] %(lineno)s %(message)s')
    # 创建控制台输出日志的handler
    ch=logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(format2)
    # 创建文件输出日志的handler
    fh=RotatingFileHandler(log_file,maxBytes=10*1024*1024,backupCount=10,encoding='utf-8') # 日志文件最大10M，最多备份5个文件
    fh.setLevel(logging.INFO)
    fh.setFormatter(format1)
    # 为logging添加handler
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

if __name__=='__main__':
    mylogger=get_logger('666')
    mylogger.debug('Test start !')
    mylogger.info('Test start !')
    mylogger.error('Test start !')
    mylogger2=get_logger('logconfig')
    mylogger2.info('Test start !')