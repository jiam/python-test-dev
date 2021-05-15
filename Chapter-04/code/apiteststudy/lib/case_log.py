from apiteststudy.config.config import logger
import os.path

def case_log(data):
    url = data['url']
    feature = data['feature']
    test_desc = data['test_desc']
    input_args = data['input_args']
    expire_result = data['expire_result']
    logger.info("%s 测试开始" % feature)
    logger.info("%s 开始" % test_desc)
    logger.info("url: %s" % url)
    logger.info("入参: %s" % input_args)
    logger.info("期望结果:%s" % expire_result)

if __name__ == "__main__":
    from apiteststudy.config.config import datapath
    from readexceldata import excel_to_list, get_test_data
    file = os.path.join(datapath, '接口测试用例.xls')
    tag = 'user'
    test_list = excel_to_list(file, tag)
    # print test_list
    data = get_test_data('create_user', test_list)
    case_log(data)