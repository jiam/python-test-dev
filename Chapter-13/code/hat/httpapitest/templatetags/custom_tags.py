import json

from django import template
from httpapitest.utils import update_include
from httpapitest.models import Module,TestCase

register = template.Library()

@register.filter(name='convert_eval')
def convert_eval(value):
    """
    数据eval转换 自建filter
    :param value:
    :return: the value which had been eval
    """
    return update_include(eval(value))

@register.filter(name='data_type')
def data_type(value):
    """
    返回数据类型 自建filter
    :param value:
    :return: the type of value
    """
    return str(type(value).__name__)

@register.filter(name='is_del')
def id_del(value):
    if value.endswith('已删除'):
        return True
    else:
        return False


@register.filter(name='json_dumps')
def json_dumps(value):
    return json.dumps(value, indent=4, separators=(',', ': '), ensure_ascii=False)


@register.filter(name='project_sum')
def project_sum(pro_name):
   
    module_count = str(Module.objects.filter(belong_project__project_name__exact=pro_name).count())
    test_count = str(TestCase.objects.filter(belong_project__exact=pro_name).count())
    sum = module_count +  '/' + test_count
    return sum


@register.filter(name='module_sum')
def module_sum(id):
    module = Module.objects.get(id=id)
    test_count = str(TestCase.objects.filter(belong_module=module).count())
    sum = test_count
    return sum