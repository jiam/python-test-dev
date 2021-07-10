import logging
from django.db import DataError
from django.core.exceptions import ObjectDoesNotExist
from httpapitest.models import TestCase, Module



logger = logging.getLogger('httpapitest.utils')
def type_change(type, value):
    """
    数据类型转换
    :param type: str: 类型
    :param value: object: 待转换的值
    :return: ok or error
    """
    try:
        if type == 'float':
            value = float(value)
        elif type == 'int':
            value = int(value)
    except ValueError:
        logger.error('{value}转换{type}失败'.format(value=value, type=type))
        return 'exception'
    if type == 'boolean':
        if value == 'False':
            value = False
        elif value == 'True':
            value = True
        else:
            return 'exception'
    return value

def key_value_dict(keyword, **kwargs):
    """
    字典二次处理
    :param keyword: str: 关键字标识
    :param kwargs: dict: 原字典值
    :return: ok or tips
    """
    if not isinstance(kwargs, dict) or not kwargs:
        return None
    else:
        dicts = {}
        test = kwargs.pop('test')
        for value in test:
            key = value.pop('key')
            val = value.pop('value')
            if 'type' in value.keys():
                type = value.pop('type')
            else:
                type = 'str'

            if key != '':
                if keyword == 'headers':
                    value[key] = val
                elif keyword == 'data':
                    msg = type_change(type, val)
                    if msg == 'exception':
                        return '{keyword}: {val}格式错误,不是{type}类型'.format(keyword=keyword, val=val, type=type)
                    value[key] = msg
                dicts.update(value)
        return dicts

def key_value_list(keyword, **kwargs):
    """
    dict change to list
    :param keyword: str: 关键字标识
    :param kwargs: dict: 待转换的字典
    :return: ok or tips
    """
    if not isinstance(kwargs, dict) or not kwargs:
        return None
    else:
        lists = []
        test = kwargs.pop('test')
        for value in test:
            if keyword == 'setup_hooks':
                if value.get('key') != '':
                    lists.append(value.get('key'))
            elif keyword == 'teardown_hooks':
                if value.get('value') != '':
                    lists.append(value.get('value'))
            else:
                key = value.pop('key')
                val = value.pop('value')
                if 'type' in value.keys():
                    type = value.pop('type')
                else:
                    type = 'str'
                tips = '{keyword}: {val}格式错误,不是{type}类型'.format(keyword=keyword, val=val, type=type)
                if key != '':
                    if keyword == 'validate':
                        value['check'] = key
                        msg = type_change(type, val)
                        if msg == 'exception':
                            return tips
                        value['expect'] = msg
                    elif keyword == 'extract':
                        value[key] = val
                    elif keyword == 'variables':
                        msg = type_change(type, val)
                        if msg == 'exception':
                            return tips
                        value[key] = msg
                    elif keyword == 'parameters':
                        try:
                            if not isinstance(eval(val), list):
                                return '{keyword}: {val}格式错误'.format(keyword=keyword, val=val)
                            value[key] = eval(val)
                        except Exception:
                            logging.error('{val}->eval 异常'.format(val=val))
                            return '{keyword}: {val}格式错误'.format(keyword=keyword, val=val)

                lists.append(value)
        return lists 


def case_logic(type=True, **kwargs):
    """
    用例信息逻辑处理以数据处理
    :param type: boolean: True 默认新增用例信息， False: 更新用例
    :param kwargs: dict: 用例信息
    :return: str: ok or tips
    """
    test = kwargs.pop('test')
    
    logger.info('用例原始信息: {kwargs}'.format(kwargs=kwargs))
    if test.get('name').get('case_name') is '':
        return '用例名称不可为空'
    if test.get('name').get('module') == '请选择':
        return '请选择或者添加模块'
    if test.get('name').get('project') == '请选择':
        return '请选择项目'
    if test.get('name').get('project') == '':
        return '请先添加项目'
    if test.get('name').get('module') == '':
        return '请添加模块'
    name = test.pop('name')
    test.setdefault('name', name.pop('case_name'))
    test.setdefault('case_info', name)
    validate = test.pop('validate')
    if validate:
        validate_list = key_value_list('validate', **validate)
        if not isinstance(validate_list, list):
            return validate_list
        test.setdefault('validate', validate_list)
    extract = test.pop('extract')
    if extract:
        test.setdefault('extract', key_value_list('extract', **extract))
    request_data = test.get('request').pop('request_data')
    data_type = test.get('request').pop('type')
    if request_data and data_type:
        if data_type == 'json':
            test.get('request').setdefault(data_type, request_data)
        else:
            data_dict = key_value_dict('data', **request_data)
            if not isinstance(data_dict, dict):
                return data_dict
            test.get('request').setdefault(data_type, data_dict)
    headers = test.get('request').pop('headers')
    if headers:
        test.get('request').setdefault('headers', key_value_dict('headers', **headers))
    variables = test.pop('variables')
    if variables:
        variables_list = key_value_list('variables', **variables)
        if not isinstance(variables_list, list):
            return variables_list
        test.setdefault('variables', variables_list)
    parameters = test.pop('parameters')
    if parameters:
        params_list = key_value_list('parameters', **parameters)
        if not isinstance(params_list, list):
            return params_list
        test.setdefault('parameters', params_list)
    hooks = test.pop('hooks')
    if hooks:
        setup_hooks_list = key_value_list('setup_hooks', **hooks)
        if not isinstance(setup_hooks_list, list):
            return setup_hooks_list
        test.setdefault('setup_hooks', setup_hooks_list)
        teardown_hooks_list = key_value_list('teardown_hooks', **hooks)
        if not isinstance(teardown_hooks_list, list):
            return teardown_hooks_list
        test.setdefault('teardown_hooks', teardown_hooks_list)
    kwargs.setdefault('test', test)
    return add_case_data(type, **kwargs)

def add_case_data(type, **kwargs):
    """
    用例信息落地
    :param type: boolean: true: 添加新用例， false: 更新用例
    :param kwargs: dict
    :return: ok or tips
    """
    case_info = kwargs.get('test').get('case_info')
    case_opt = TestCase.objects
    name = kwargs.get('test').get('name')
    module = case_info.get('module')
    project = case_info.get('project')
    belong_module = Module.objects.get(id=int(module))
    config = case_info.get('config', '')
    if config != '':
        case_info.get('include')[0] = eval(config)

    try:
        if type:

            if case_opt.get_case_name(name, module, project) < 1:
                case_opt.insert_case(belong_module, **kwargs)
                logger.info('{name}用例添加成功: {kwargs}'.format(name=name, kwargs=kwargs))
            else:
                return '用例已存在，请重新编辑'
        else:
            index = case_info.get('test_index')
            if name != case_opt.get(id=index).name \
                    and case_opt.get_case_name(name, module, project) > 0:
                return '用例已在该模块中存在，请重新命名'
            case_opt.update_case(belong_module, **kwargs)
            logger.info('{name}用例更新成功: {kwargs}'.format(name=name, kwargs=kwargs))

    except DataError:
        logger.error('用例信息：{kwargs}过长！！'.format(kwargs=kwargs))
        return '字段长度超长，请重新编辑'
    return 'ok'


def update_include(include):
    for i in range(0, len(include)):
        id = include[i][0]
        source_name = include[i][1]
        try:
            name = TestCase.objects.get(id=id).name
        except ObjectDoesNotExist:
            name = source_name + ' 已删除'
            logger.warning('依赖的 {name} 用例已经被删除啦！！'.format(name=source_name))        
        include[i] = [id, name]

    return include