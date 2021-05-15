import os
from lib.log_config import get_logger
from lib.send_email import send_mail
from run_case import run_case
from save_result import save_result


'''
自动化测试执行入口
用例文件为:./testcase/testcase.xls
测试结果存放目录：./result
'''
_mylogger = get_logger(os.path.basename(__file__))


if __name__ == '__main__':
    rootPath = os.path.split(os.path.realpath(__file__))[0]
    _mylogger.info('主目录：'+rootPath)
    casePath = os.path.join(rootPath,'testcase')
    resultPath = os.path.join(rootPath,'result')
    caseFile = os.path.join(casePath,'testcase.xls')
    print('caseFile:'+caseFile)
    run = run_case()

    if os.path.exists(caseFile):
        # 打开excel文件读取数据
        stepResult, caseResult = run.run_test(caseFile)
        reportFile = save_result(caseFile, stepResult, caseResult, resultPath)
        # 邮件发送测试报告
        _mylogger.info(reportFile)
        send_mail(sub='测试报告', content='测试详情见附件', reportFile = reportFile)
    else:
        _mylogger.error('获取用例文件失败')
        exit()


