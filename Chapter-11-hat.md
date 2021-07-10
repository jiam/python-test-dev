# 实战http接口测试平台HAT

## 模块管理功能
模块的增删改查

### 创建模块的相关model 类

```python
class Module(BaseTable):
    class Meta:
        verbose_name = '模块信息'
        db_table = 'Module'

    module_name = models.CharField('模块名称', max_length=50, null=False)
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    test_user = models.CharField('测试负责人', max_length=50, null=False)
    simple_desc = models.CharField('简要描述', max_length=100, null=True)
    other_desc = models.CharField('其他信息', max_length=100, null=True)

```

执行数据迁移命令
```shell
python  manage.py makemigrations
python  manage.py migrate
```

### 定义视图
先定义空视图
```python
def module_add(request):
    pass

def module_list(request):
    pass

def module_search_ajax(request):
    pass

def module_edit(request):
    pass

def module_delete(request):
    pass

```

### 定义url
```python
    path('module/list', views.module_list, name='module_list'),
    path('module/add', views.module_add, name='module_add'),
    path('module/edit', views.module_edit, name='module_edit'),
    path('module/delete', views.module_delete, name='module_delete'),   
```
### 修改module_add视图

```
@csrf_exempt
def module_add(request):
    if request.method == 'GET':
        projects = Project.objects.all().order_by("-update_time")
        context_dict = {'data': projects}
        return render(request, 'module_add.html',context_dict)
    if request.is_ajax():
        module = json.loads(request.body.decode('utf-8'))
        if module.get('module_name') == '':
            msg = '模块名称不能为空'
            return HttpResponse(msg)
        if module.get('belong_project') == '请选择':
            msg = '请选择项目，没有请先添加哦'
            return HttpResponse(msg)
        if module.get('test_user') == '':
            msg = '测试人员不能为空'
            return HttpResponse(msg)
        p = Project.objects.get(project_name=module.get('belong_project'))
        if Module.objects.filter(module_name=module.get('module_name'), belong_project=p):
            msg = "项目已经存在"
            return HttpResponse(msg)
        else:
            m = Module()
            m.module_name = module.get('module_name')
            p = Project.objects.get(project_name=module.get('belong_project'))
            m.belong_project = p
            m.test_user = module.get('test_user')
            m.simple_desc = module.get('simple_desc')
            m.other_desc = module.get('other_desc')
            m.save()
            msg = 'ok'
        if msg == 'ok':
            return HttpResponse(reverse('module_list'))
        else:
            return HttpResponse(msg)
```
导入 Module 模型类
修改`from httpapitest.models import Project, DebugTalk,`为
`from httpapitest.models import Project, DebugTalk, Module`

### 添加module_add.html模板
```python
{% extends "base.html" %}
{% block title %}新增模块{% endblock %}
{% load staticfiles %}
{% block content %}

    <div class=" admin-content">

        <div class="admin-biaogelist">
            <div class="listbiaoti am-cf">
                <ul class="am-icon-flag on"> 新增模块</ul>
                <dl class="am-icon-home" style="float: right;"> 当前位置： 模块管理&gt;新增模块</dl>
            </div>
            <div class="fbneirong">
                <form class="form-horizontal" id="module_add">
                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="module_name">模块名称：</label>
                        <div class="col-md-5">
                            <input type="text" class="form-control" id="module_name"
                                   aria-describedby="inputSuccess3Status" name="module_name" placeholder="请输入模块名称"
                                   value="">
                            <span class="glyphicon glyphicon-th-list form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-2 text-primary" for="belong_project">所属项目：</label>
                        <div class="col-md-5">
                            <select name="belong_project" class="form-control">
                                <option value="请选择">请选择</option>
                                {% for foo in  data %}
                                    <option value="{{ foo.project_name }}">{{ foo.project_name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>

                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="test_user">测试人员：</label>
                        <div class="col-md-5">
                            <input type="text" class="form-control" id="test_user" name="test_user"
                                   aria-describedby="inputSuccess3Status" placeholder="请输入参与的测试人员" value="">
                            <span class="glyphicon glyphicon-user form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>

                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="simple_desc">简要描述：</label>
                        <div class="col-md-5">
                            <textarea type="text" rows="3" class="form-control" id="simple_desc" name="simple_desc"
                                      aria-describedby="inputSuccess3Status" placeholder="模块简单概述"></textarea>
                            <span class="glyphicon glyphicon-paperclip form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>

                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="other_desc">其他信息：</label>
                        <div class="col-md-5">
                            <textarea type="text" rows="3" class="form-control" id="other_desc" name="other_desc"
                                      aria-describedby="inputSuccess3Status" placeholder="模块其他相关信息描述"></textarea>
                            <span class="glyphicon glyphicon-paperclip form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>
                    <div class="am-form-group am-cf">
                        <div class="you" style="margin-left: 8%;">
                            <button type="button" class="am-btn am-btn-success am-radius"
                                    onclick="module_add('#module_add', '{% url 'module_add' %}')">点 击 提 交
                            </button>&nbsp;
                            &raquo; &nbsp;
                            <a type="submit" href="#" class="am-btn am-btn-secondary am-radius">新 增 用 例</a>

                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>

{% endblock %}
```

### commons.js添加 
```js
/*添加模块*/
function module_add(url) {
    // 使用jquery获取表单数据
    var data = $('#module_add').serializeJSON(); 

    // 对表单数据做校验
    if (data.module_name === '' ) {
        myAlert('模块名称不能为空')
        return
    }
    if (data.belong_project === '请选择') {
        myAlert('请选择项目，没有请先添加哦')
        return
    }

    if (data.test_user === '') {
        myAlert('测试人员不能为空')
        return
    }

    // 使用jquery的ajax 提交表单
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data.indexOf('/httpapitest/') !== -1) {
                window.location.href = data;
            } else {
                myAlert(data);
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}
```

验证添加模块功能
访问`http://127.0.0.1:8000/httpapitest/module/add`

会得到报错`The view httpapitest.views.module_list didn't return an HttpResponse object. It returned None instead` 因为 module_list视图还没有实现功能

### 修改module_list视图

```python
@csrf_exempt
def module_list(request):
    if request.method == 'GET':
        module = request.GET.get("module", "")
        if module:
            rs = Module.objects.filter(module_name__contains=module).order_by("-update_time")
        else:
            rs = Module.objects.all().order_by("-update_time")
        info = {'module': module}
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        context_dict = {'modules': objects,'info': info }
        return render(request,"module_list.html",context_dict)
```
### 添加module_list.html 模板
```html
{% extends "base.html" %}
{% block title %}模块信息{% endblock %}
{% load staticfiles %}
{% block content %}
    <div class="am-modal am-modal-prompt" tabindex="-1" id="my-edit">
        <div class="am-modal-dialog">
            <div style="font-size: medium;" class="am-modal-hd">HAT</div>
            <div class="am-modal-bd">
                <form class="form-horizontal" id="edit_form">
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="index"
                               style="font-weight: inherit; font-size: small " hidden>索引值：</label>
                        <div class="col-sm-9">
                            <input name="index" type="text" class="form-control" id="index"
                                   placeholder="索引值" hidden value="">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="module_name"
                               style="font-weight: inherit; font-size: small ">模块名称：</label>
                        <div class="col-sm-9">
                            <input name="module_name" type="text" class="form-control" id="module_name"
                                   placeholder="模块名称" value="">
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="control-label col-sm-3" for="belong_project"
                               style="font-weight: inherit; font-size: small ">所属项目：</label>
                        <div class="col-sm-9">
                            <input name="belong_project" type="text" id="belong_project" class="form-control"
                                   placeholder="所属项目" readonly>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="control-label col-sm-3" for="test_user"
                               style="font-weight: inherit; font-size: small ">测试人员：</label>
                        <div class="col-sm-9">
                            <input name="test_user" type="text" id="test_user" class="form-control"
                                   placeholder="测试人员" value="">
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="control-label col-sm-3" for="simple_desc"
                               style="font-weight: inherit; font-size: small ">简要描述：</label>
                        <div class="col-sm-9">
                            <input name="simple_desc" type="text" id="simple_desc" class="form-control"
                                   placeholder="简要描述" value="">
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="control-label col-sm-3" for="other_desc"
                               style="font-weight: inherit; font-size: small ">其他信息：</label>
                        <div class="col-sm-9">
                            <input name="other_desc" type="text" id="other_desc" class="form-control"
                                   placeholder="其他信息" value="">
                        </div>
                    </div>

                </form>
            </div>
            <div class="am-modal-moduleter">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>提交</span>
            </div>
        </div>
    </div>
        <div class="am-modal am-modal-confirm" tabindex="-1" id="delete-tip">
        <div class="am-modal-dialog">
            <div class="am-modal-hd">HAT</div>
            <div class="am-modal-bd">
                亲，此操作会删除该模块下所有用例和配置，请谨慎操作！！！
            </div>
            <div class="am-modal-moduleter">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>确定</span>
            </div>
        </div>
    </div>

    <div class="am-modal am-modal-confirm" tabindex="-1" id="select_env">
        <div class="am-modal-dialog">
            <div class="am-modal-hd">HAT</div>
            <form class="form-horizontal">
                <div class="form-group">
                    <label class="control-label col-sm-3" for="report_name"
                           style="font-weight: inherit; font-size: small ">报告名称：</label>
                    <div class="col-sm-8">
                        <input name="report_name" type="text" id="report_name" class="form-control"
                               placeholder="默认时间戳命名" value="" readonly>
                    </div>
                </div>

                <div class="form-group">
                    <label class="control-label col-sm-3"
                           style="font-weight: inherit; font-size: small ">执行方式:</label>
                    <div class="col-sm-8">
                        <select class="form-control" id="mode" name="mode">
                            <option value="true">同步(执行完立即返回报告)</option>
                            <option value="false">异步(后台执行，完毕后可查看报告)</option>
                        </select>
                    </div>
                </div>
            </form>
            </form>

            <div class="am-modal-moduleter">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>确定</span>
            </div>
        </div>
    </div>


    <div class="admin-biaogelist">
        <div class="listbiaoti am-cf">
            <ul class="am-icon-flag on"> 模块列表</ul>
            <dl class="am-icon-home" style="float: right;"> 当前位置： 模块管理 > <a href="#">模块展示</a></dl>
            <dl>
                <button type="button" class="am-btn am-btn-danger am-round am-btn-xs am-icon-plus"
                        onclick="location='{% url 'module_add' %}'">新增模块
                </button>
                <button type="button" class="am-btn am-btn-danger am-round am-btn-xs am-icon-bug"
                         onclick="#">运行
                </button>

            </dl>
        </div>

        <div class="am-btn-toolbars am-btn-toolbar am-kg am-cf">
            <form id="pro_filter">
                <ul>
                    <li style="padding-top: 5px"><input value="{{ info.module }}" type="text" name="module"
                                                        class="am-input-sm am-input-xm"
                                                        placeholder="模块名称"/></li>
                    <li>
                        <button style="padding-top: 5px; margin-top: 9px"
                                class="am-btn am-radius am-btn-xs am-btn-success">搜索
                        </button>
                    </li>
                </ul>
            </form>
        </div>


        <form class="am-form am-g" id='module_list' name="module_list" >
            <table width="100%" class="am-table am-table-bordered am-table-radius am-table-striped">
                <thead>
                <tr class="am-success">
                    <th class="table-check"><input type="checkbox" id="select_all"/></th>
                    <th class="table-title">序号</th>
                    <th class="table-type">模块名称</th>
                    <th class="table-type">测试人员</th>
                    <th class="table-type">所属项目</th>
                    <th class="table-type">用例</th>
                    <th class="table-date am-hide-sm-only">创建日期</th>
                    <th width="163px" class="table-set">操作</th>
                </tr>
                </thead>
                <tbody>

                {% for module in modules %}
                    <tr>
                        <td><input type="checkbox" name="module_{{ module.id }}" value="{{ module.id }}"/></td>
                        <td>{{ forloop.counter }}</td>
                        <td>{{ module.module_name }}</td>
                        <td>{{ module.test_user }}</td>
                        <td>{{ module.belong_project.project_name }}</td>
                        <td>0</td> 
                        <td class="am-hide-sm-only">{{ module.create_time }}</td>
                        <td>
                            <div class="am-btn-toolbar">
                                <div class="am-btn-group am-btn-group-xs">
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-secondary am-round"
                                            data-am-popover="{content: '运行', trigger: 'hover focus'}"
                                            onclick="#"
                                            >
                                        <span class="am-icon-bug"></span>
                                    </button>
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-secondary am-round"
                                            data-am-popover="{content: '编辑', trigger: 'hover focus'}"
                                            onclick="edit('{{ module.id }}','{{ module.module_name }}', '{{ module.belong_project.project_name }}'
                                                    , '{{ module.test_user }}', '{{ module.simple_desc }}', '{{ module.other_desc }}')">
                                            <span class="am-icon-pencil-square-o"></span>
                                    </button>
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-danger am-round"
                                            data-am-popover="{content: '删除', trigger: 'hover focus'}"
                                            onclick="deleteModule('{{ module.id }}')">
                                            <span class="am-icon-trash-o"></span>
                                    </button>
                                </div>
                            </div>
                        </td>
                    </tr>
                {% endfor %}


                </tbody>
            </table>

            <div class="am-btn-group am-btn-group-xs">
                <button type="button" class="am-btn am-btn-default" onclick="location='{% url 'module_add' %}'"><span
                        class="am-icon-plus"></span> 新增
                </button>
            </div>

            <ul class="am-pagination am-fr">
                            <span class="step-links">
                                {% if modules.has_previous %}
                                   
                                    <a href="?page={{ modules.previous_page_number }}">上一页</a>
                                {% endif %}
                        
                                <span class="current">
                                     {{ modules.number }}/{{ modules.paginator.num_pages }} 页.
                                </span>
                        
                                {% if modules.has_next %}
                                    <a href="?page={{ modules.next_page_number }}">下一页</a>
                                    
                                {% endif %}
                            </span>
            </ul>


            <hr/>

        </form>
    </div>
    <script type="text/javascript">
       function edit(id, module_name, belong_project, test_user, simple_desc, other_desc) {
            $('#index').val(id);
            $('#module_name').val(module_name);
            $('#belong_project').val(belong_project);
            $('#test_user').val(test_user);
            $('#simple_desc').val(simple_desc);
            $('#other_desc').val(other_desc);
            $('#my-edit').modal({
                relatedTarget: this,
                onConfirm: function () {
                    update_data_ajax('#edit_form', '{% url 'module_edit' %}')
                },
                onCancel: function () {
                }
            });
        }

        function deleteModule(name) {
            $('#delete-tip').modal({
                relatedTarget: this,
                onConfirm: function () {
                    del_data_ajax(name, '{% url 'module_delete' %}')
                },
                onCancel: function () {
                }
            });
        }
        $('#mode').change(function () {
            if ($('#mode').val() == 'false') {
                $('#report_name').removeAttr("readonly");
            } else {
                $('#report_name').attr('readonly', 'readonly');
            }
        });

        

        $('#select_all').click(function () {
            var isChecked = $(this).prop("checked");
            $("input[name^='module']").prop("checked", isChecked);
        })
    </script>

{% endblock %}

```

测试 http://127.0.0.1:8000/httpapitest/module/list

### 修改base.html
修改base.html 使菜单 模块列表，和添加模块可用
```
            <ul>
                <li><a href="{% url 'module_list' %}">模 块 列 表</a></li>
                <li><a href="{% url 'module_add' %}">新 增 模 块</a></li>
            </ul>
```

### 修改moddule_edit视图
```python
@csrf_exempt
def module_edit(request):
    if request.is_ajax():
        module = json.loads(request.body.decode('utf-8'))
        
        if module.get('module_name') == '':
            msg = '模块名称不能为空'
            return HttpResponse(msg)
        if module.get('belong_project') == '请选择':
            msg = '请选择项目，没有请先添加哦'
            return HttpResponse(msg)
        if module.get('test_user') == '':
            msg = '测试人员不能为空'
            return HttpResponse(msg)
        p = Project.objects.get(project_name=module.get('belong_project'))
        if module.get('module_name') != Module.objects.get(id=module.get('index')).module_name and \
            Module.objects.filter(module_name=module.get('module_name'), belong_project=p).count()>0:
            msg = "模块已经存在"
            return HttpResponse(msg)
        else:
            m = Module.objects.get(id=module.get('index'))
            m.module_name = module.get('module_name')
            m.belong_project = p
            m.test_user = module.get('test_user')
            m.simple_desc = module.get('simple_desc')
            m.other_desc = module.get('other_desc')
            m.save()
            msg = 'ok'
        if msg == 'ok':
            return HttpResponse(reverse('module_list'))
        else:
            return HttpResponse(msg)
```

点击编辑测试

修改module_delete视图

```
@csrf_exempt
def module_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        project_id = data.get('id')
        module = Module.objects.get(id=project_id)
        module.delete()
        return HttpResponse(reverse('module_list'))
```

## 用例管理
测试用例的增删改查

###  添加model 类TestCase

添加Testcase类的 管理类，在httpapitest目录下创建managers.py文件
在managers.py 添加 TestCaseManager 类
```python
from django.db import models

class TestCaseManager(models.Manager):
    def insert_case(self, belong_module, **kwargs):
        case_info = kwargs.get('test').pop('case_info')
        self.create(name=kwargs.get('test').get('name'), belong_project=case_info.pop('project'),
                    belong_module=belong_module,
                    author=case_info.pop('author'), include=case_info.pop('include'), request=kwargs)

    def update_case(self, belong_module, **kwargs):
        case_info = kwargs.get('test').pop('case_info')
        obj = self.get(id=case_info.pop('test_index'))
        obj.belong_project = case_info.pop('project')
        obj.belong_module = belong_module
        obj.name = kwargs.get('test').get('name')
        obj.author = case_info.pop('author')
        obj.include = case_info.pop('include')
        obj.request = kwargs
        obj.save()

    def get_case_name(self, name, module_name, belong_project):
        return self.filter(belong_module__id=module_name).filter(name__exact=name).filter(
            belong_project__exact=belong_project).count()
```

在 models.py 添加 TestCase类
```
class TestCase(BaseTable):
    class Meta:
        verbose_name = '用例信息'
        db_table = 'TestCase'
    name = models.CharField('用例名称', max_length=50, null=False)
    belong_project = models.CharField('所属项目', max_length=50, null=False)
    belong_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    include = models.CharField('前置config/test', max_length=1024, null=True)
    author = models.CharField('创建者', max_length=20, null=False)
    request = models.TextField('请求信息', null=False)
    objects = TestCaseManager()
```
导入 TestCaseManager 类
`from httpapitest.managers import TestCaseManager`

执行数据库迁移命令


###  添加用例

1. 添加视图函数所依赖的的函数
在httpapitest 创建utils.py

```python
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


```

2. 添加视图函数 

```python
@csrf_exempt
def case_add(request):
    if request.method == 'GET':
        context_dict = {
            'projects': Project.objects.all().values('project_name').order_by('-create_time')
        }
        return render(request, 'case_add.html', context_dict)
    if request.is_ajax():
        testcase = json.loads(request.body.decode('utf-8'))
        msg = case_logic(**testcase)
        if msg == 'ok':
            return HttpResponse(reverse('case_list'))
        else:
            return HttpResponse(msg)

def case_list(request):
    pass


def case_edit(request):
    pass

def case_delete(request):
    pass

def case_copy(request):
    pass


```
导入函数case_logic
`from httpapitest.utils import case_logic_logic`
导入TestCase
`from httpapitest.models import Project, DebugTalk, Module`为
`from httpapitest.models import Project, DebugTalk, Module,TestCase`





4. 添加模板文件 case_add.html
```html
{% extends "base.html" %}
{% block title %}新增用例{% endblock %}
{% load staticfiles %}



{% block content %}

    <div class="am-modal am-modal-confirm" tabindex="-1" id="save_test">
        <div class="am-modal-dialog">
            <div class="am-modal-hd">HAT</div>
            <form class="form-horizontal" id="form_message">
                <div class="form-group" style="display: none">
                    <div class="input-group col-md-4 col-md-offset-1">
                        <div class="input-group-addon" style="color: #0a628f;">编写人员</div>
                        <input type="text" class="form-control" id="author" name="author"
                               placeholder="" value="test">
                    </div>
                </div>

                <div class="form-group">
                    <label class="control-label col-sm-3" for="case_name"
                           style="font-weight: inherit; font-size: small ">用例名称:</label>
                    <div class="col-sm-8">
                        <input name="case_name" type="text" class="form-control" id="case_name"
                               placeholder="给用例起个名吧" value="">
                    </div>
                </div>

                <div class="form-group">
                    <label class="control-label col-sm-3"
                           style="font-weight: inherit; font-size: small ">选择项目:</label>
                    <div class="col-sm-8">
                        <select class="form-control"  name="project"
                                onchange="auto_load('#form_message', '{%  url 'module_search_ajax' %}', '#module', 'module')">
                            <option value="请选择">请选择</option>
                            {% for foo in projects %}
                                <option value="{{ foo.project_name }}">{{ foo.project_name }}</option>
                            {% endfor %}
                        </select>
                    </div>

                </div>

                <div class="form-group">
                    <label class="control-label col-sm-3"
                           style="font-weight: inherit; font-size: small ">选择模块:</label>
                    <div class="col-sm-8">
                        <select class="form-control" id="module" name="module">
                        </select>
                    </div>

                </div>


            </form>
            <div class="am-modal-footer">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>确定</span>
            </div>
        </div>
    </div>

    <div class="admin-biaogelist" xmlns="http://www.w3.org/1999/html" xmlns="http://www.w3.org/1999/html">

        <div class="listbiaoti am-cf">
            <ul class="am-icon-flag on"> 用例编辑</ul>
            <dl class="am-icon-home" style="float: right;">当前位置： 用例管理 > <a href="#">新增用例</a></dl>
        </div>

        <div class="am-tabs am-margin">
            <ul class="am-tabs-nav am-nav am-nav-tabs" id="tab-test">
               
                <li><a href="javascript:;" data-target="#tab3">请求</a></li>
                <li><a href="javascript:;" data-target="#tab4">提取/验证</a></li>
                <li><a href="javascript:;" data-target="#tab2">变量/hooks</a></li>
                <li><a href="javascript:;" data-target="#tab1">依赖信息</a></li>
            </ul>

            <div class="am-tabs-bd">
                <div class="am-tab-panel" id="tab1">
                    <div style="float: left; width: 40%;">
                        <form class="form-horizontal" id="belong_message">
                            <div class="form-group">
                                <div class="input-group col-md-10 col-md-offset-1">
                                    <div class="input-group-addon" style="color: #0a628f">所属项目</div>
                                    <select  name="project" class="form-control"
                                            onchange="auto_load('#belong_message', '{% url 'module_search_ajax' %}', '#belong_module_id', 'module')">
                                        <option value="请选择">请选择</option>
                                        {% for foo in projects %}
                                            <option value="{{ foo.project_name }}">{{ foo.project_name }}</option>
                                        {% endfor %}
                                    </select>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="input-group col-md-10 col-md-offset-1">
                                    <div class="input-group-addon" style="color: #0a628f">可选模块</div>
                                    <select id="belong_module_id" name="module" class="form-control"
                                            onchange="auto_load('#belong_message', '{% url 'case_search_ajax'%}', '#belong_case_id', 'case');">
                                    </select>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="input-group col-md-10 col-md-offset-1">
                                    <div class="input-group-addon" style="color: #0a628f">可选用例</div>
                                    <select id="belong_case_id" name="include" class="form-control">
                                    </select>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div style="float: right; width: 50%;margin-right: 1%;">
                         <div class="form-group">
                                <div class="input-group col-md-10 ">
                                    <div class="input-group-addon" id="close_collapse" style="color: #0a628f">用例列表</div>

                                    <a class="am-btn am-btn-primary am-radius am-btn-block" href="#" id="pre_collapse"
                                       style="font-size: 16px; background-color: #fff; color: #555; text-align: left"
                                       data-am-collapse="{target: '#pre_case'}">
                                        用 例 执 行 顺 序
                                    </a>
                                    <nav>
                                        <ul id="pre_case" class="am-nav">
                                        </ul>
                                    </nav>

                                </div>
                            </div>
                    </div>
                </div>

                <div class="am-tab-panel" id="tab2">
                    <button class="btn btn-info" value="添 加" onclick="add_row('variables')">add variables</button>
                    <button class="btn btn-danger" value="删 除" onclick="del_row('variables')">del variables</button>
                    <button class="btn btn-info" value="添 加" onclick="add_row('hooks')">add hooks</button>
                    <button class="btn btn-danger" value="删 除" onclick="del_row('hooks')">del hooks</button>

                    <form id="form_variables">
                        <table class="table table-hover table-condensed table-bordered table-striped" id="variables">
                            <caption>Variables:</caption>
                            <thead>
                            <tr class="active text-success">
                                <th width="5%" align="center">Option</th>
                                <th width="30%" align="center">Key</th>
                                <th width="10%" align="center">Type</th>
                                <th width="55%" align="center">Value</th>
                            </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </form>


                    <form id="form_hooks">
                        <table class="table table-hover table-condensed table-bordered table-striped" id="hooks">
                            <caption>hooks:</caption>
                            <thead>
                            <tr class="active text-success">
                                <th width="5%" align="center">Option</th>
                                <th width="47.5%" align="center">setup_hooks</th>
                                <th width="47.5%" align="center">teardown_hooks</th>
                            </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </form>

                </div>

                <div class="am-tab-panel" id="tab3">
                    <div class="form-inline">
                        <div class="form-group">
                            <div class="input-group">
                                <div class="input-group-addon">URL</div>
                                <input type="text" class="form-control" id="url" name="url" placeholder="api url">
                            </div>
                        </div>

                        <div class="form-group ">
                            <div class="input-group">
                                <div class="input-group-addon">Method</div>
                                <select class="form-control" name="method" id="method">
                                    <option>POST</option>
                                    <option>GET</option>
                                    <option>PUT</option>
                                    <option>DELETE</option>
                                </select>
                            </div>
                        </div>

                        <div class="form-group ">
                            <div class="input-group">
                                <div class="input-group-addon">Type</div>
                                <select class="form-control" name="DataType" id="DataType">
                                    <option>data</option>
                                    <option>json</option>
                                    <option>params</option>
                                </select>
                            </div>
                        </div>

                        <button class="btn btn-info" value="添 加" id="add_data" onclick="add_row('data')">add data
                        </button>
                        <button class="btn btn-danger" value="删 除" id="del_data" onclick="del_row('data')">del data
                        </button>
                        <button class="btn btn-info" value="添 加" onclick="add_row('header')">add headers</button>
                        <button class="btn btn-danger" value="删 除" onclick="del_row('header')">del headers</button>

                        <form id="form_request_data">
                            <table class="table table-hover table-condensed table-bordered table-striped" id="data">
                                <caption>data:</caption>
                                <thead>
                                <tr class="active text-success">
                                    <th width="5%" align="center">Option</th>
                                    <th width="30%" align="center">Key</th>
                                    <th width="5%" align="center">Type</th>
                                    <th width="60%" align="center">Value</th>
                                </tr>
                                </thead>
                                <tbody>
                                </tbody>
                            </table>
                        </form>

                        <form id="form_request_headers">
                            <table class="table table-hover table-condensed table-bordered table-striped" id="header">
                                <caption>headers:</caption>
                                <thead>
                                <tr class="active text-success">
                                    <th width="5%" align="center">Option</th>
                                    <th width="40%" align="center">Key</th>
                                    <th width="55%" align="center">Value</th>
                                </tr>
                                </thead>
                                <tbody>
                                </tbody>
                            </table>
                        </form>
                    </div>
                </div>
                <div class="am-tab-panel" id="tab4">
                    <button class="btn btn-info" value="添 加" onclick="add_row('extract')">add extract
                    </button>
                    <button class="btn btn-danger" value="删 除" onclick="del_row('extract')">del extract
                    </button>
                    <button class="btn btn-info" value="添 加" onclick="add_row('validate')">add validate</button>
                    <button class="btn btn-danger" value="删 除" onclick="del_row('validate')">del validate</button>
                    <form id="form_extract">
                        <table class="table table-hover table-condensed table-bordered table-striped" id="extract">
                            <caption>extract:</caption>
                            <thead>
                            <tr class="active text-success">
                                <th width="5%" align="center">Option</th>
                                <th width="30%" align="center">Key</th>
                                <th width="55%" align="center">Value</th>
                            </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </form>

                    <form id="form_validate">
                        <table class="table table-hover table-condensed table-bordered table-striped" id="validate">
                            <caption>validate:</caption>
                            <thead>
                            <tr class="active text-success">
                                <th width="2%" align="center">Option</th>
                                <th width="32%" align="center">Check</th>
                                <th width="10%" align="center">Comparator</th>
                                <th width="8%" align="center">Type</th>
                                <th width="48%" align="center">Expected</th>
                            </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </form>

                </div>
            </div>

        </div>

        <div class="am-form-group am-cf">
            <div class="you" style="margin-left: 11%;">
                <button id="save" type="button" class="am-btn am-btn-success am-radius">点 击 提 交
                </button>&nbsp;
                &raquo; &nbsp;
                <a type="submit" href="{% url 'case_add'%}" class="am-btn am-btn-secondary am-radius">新 增 配 置</a>

            </div>
        </div>
    </div>
    <script>
        editor = null;

        $('#DataType').on('change', function () {
            if ($('#DataType').val() === 'json') {
                $('#add_data').attr('disabled', true);
                $('#del_data').attr('disabled', true);
                $('#data').remove();
                var json_text = "<span style=\"font-size:10px;\" id=\"json-text\">\n" +
                    " <div style=\"margin-left: 0px; margin-top: 5px; height: 200px\">" +
                    "<pre id=\"code\" class=\"ace_editor\" style=\"margin-top: 0px; margin-bottom: 0px; min-height: 200px;\">\n" +
                    "<textarea>\n" +
                    "{\"key\":\"value\"}\n" +
                    "</textarea>\n" +
                    "</pre></div></span>";

                $('#form_request_data').append(json_text);

                editor = ace.edit("code");
                init_acs('json', 'github', editor);

            } else {
                var table = '<table class="table table-hover table-condensed table-bordered table-striped" id="data">\n' +
                    '                                <caption>' + $('#DataType').val() + ':</caption>\n' +
                    '                                <thead>\n' +
                    '                                <tr class="active text-success">\n' +
                    '                                    <th width="5%" align="center">Option</th>\n' +
                    '                                    <th width="30%" align="center">Key</th>\n' +
                    '                                    <th width="5%" align="center">Type</th>\n' +
                    '                                    <th width="60%" align="center">Value</th>\n' +
                    '                                </tr>\n' +
                    '                                </thead>\n' +
                    '                                <tbody>\n' +
                    '                                </tbody>\n' +
                    '                            </table>';

                $('#add_data').text('add ' + $('#DataType').val());
                $('#del_data').text('del ' + $('#DataType').val());

                $('#add_data').removeAttr("disabled");
                $('#del_data').removeAttr("disabled");
                $('#data').remove();
                $('#json-text').remove();
                $('#form_request_data').append(table);
            }
        });

        $("#tab-test").on("click", "li", function () {
            $(this).addClass("am-active").siblings("li").removeClass("am-active");
            var target = $(this).children("a").attr("data-target");
            $(target).addClass("am-active").siblings(".am-tab-panel").removeClass("am-active");
        }).find("li").eq(0).trigger("click");

        $(function () {
            $("#pre_case").sortable();
            $("#pre_case").disableSelection();
        });

        $('#config').on('change', function () {
            if ($('#config').val() !== '请选择') {
                var case_id = $('#config').val();
                var case_name = $('#config option:selected').text();
                var href = "<li disbaled id=" + case_id + " name='pre_config'><a style='color: cadetblue' href='/httpapitest/config/edit/" + case_id + "' id = " + case_id + ">" + case_name + "" +
                    "</a><i class=\"js-remove\" onclick=remove_self('#" + case_id + "')>✖</i></li>";
                $("li[name='pre_config']").remove();
                $("#pre_case").prepend(href);
                $('#config_pre').val("{'config': ['" + case_id + "', '" + case_name + "']}");
            }
        });

        $("li[name='pre_config'] a i").on('click', function () {
            $('#config_pre').val("");
        });

        $('#belong_case_id').on('change', function () {
            if ($('#belong_case_id').val() !== '请选择') {
                var case_id = $('#belong_case_id').val();
                var case_name = $('#belong_case_id option:selected').text();
                var href = "<li id=" + case_id + "><a href='/httpapitest/case/edit/" + case_id + "' id = " + case_id + ">" + case_name + "" +
                    "</a><i class=\"js-remove\" onclick=remove_self('#" + case_id + "')>✖</i></li>";
                $("#pre_case").append(href);
            }
        });

        function remove_self(id) {
            $(id).remove();
        }

        $('#save').on('click', function () {
            if ($("li[name='pre_config']").length <= 0) {
                $('#config_pre').val("");
            }
            $('#save_test').modal({
                relatedTarget: this,
                onConfirm: function () {
                    case_ajax('add', editor)
                },
                onCancel: function () {
                }
            });
        })

    </script>


{% endblock %}

```

5. 在views.py添加module_search_ajax,case_search_ajax
```python
@csrf_exempt
def case_add(request):
    if request.method == 'GET':
        context_dict = {
            'projects': Project.objects.all().values('project_name').order_by('-create_time')
        }
        return render(request, 'case_add.html', context_dict)
    if request.is_ajax():
        testcase = json.loads(request.body.decode('utf-8'))
        msg = case_logic(**testcase)
        if msg == 'ok':
            return HttpResponse(reverse('case_list'))
        else:
            return HttpResponse(msg)

@csrf_exempt
def module_search_ajax(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        if 'case' in data.keys():
            project = data["case"]["name"]["project"]
        if 'crontab' in data.keys():
            project = data["crontab"]["name"]["project"]
        if  project != "All" and project != "请选择":
            p = Project.objects.get(project_name=project)
            modules = Module.objects.filter(belong_project=p)
            modules_list = ['%d^=%s' % (m.id, m.module_name) for m in modules ]
            modules_string = 'replaceFlag'.join(modules_list)
            return HttpResponse(modules_string)
        else:
            return HttpResponse('')

@csrf_exempt
def case_search_ajax(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        if 'case' in data.keys():
            project = data["case"]["name"]["project"]
            module = data["case"]["name"]["module"]
        if   project != "请选择" and module != "请选择":
            m = Module.objects.get(id=module)
            cases = TestCase.objects.filter(belong_project=project, belong_module=m)
            case_list = ['%d^=%s' % (c.id, c.name) for c in cases ]
            case_string = 'replaceFlag'.join(case_list)
            return HttpResponse(case_string)
        else:
            return HttpResponse('')

```



6. 在commons.js 中添加case_add.html 中使用的js 函数 
```js
function del_row(id) {
    var attribute = id;
    var chkObj = document.getElementsByName(attribute);
    var tabObj = document.getElementById(id);
    for (var k = 0; k < chkObj.length; k++) {
        if (chkObj[k].checked) {
            tabObj.deleteRow(k + 1);
            k = -1;
        }
    }
}

function add_row(id) {
    var tabObj = document.getElementById(id);//获取添加数据的表格
    var rowsNum = tabObj.rows.length;  //获取当前行数
    var style = 'width:100%; border: none';
    var cell_check = "<input type='checkbox' name='" + id + "' style='width:55px' />";
    var cell_key = "<input type='text' name='test[][key]'  value='' style='" + style + "' />";
    var cell_value = "<input type='text' name='test[][value]'  value='' style='" + style + "' />";
    var cell_type = "<select name='test[][type]' class='form-control' style='height: 25px; font-size: 15px; " +
        "padding-top: 0px; padding-left: 0px; border: none'> " +
        "<option>string</option><option>int</option><option>float</option><option>boolean</option></select>";
    var cell_comparator = "<select name='test[][comparator]' class='form-control' style='height: 25px; font-size: 15px; " +
        "padding-top: 0px; padding-left: 0px; border: none'> " +
        "<option>equals</option> <option>contains</option> <option>startswith</option> <option>endswith</option> <option>regex_match</option> <option>type_match</option> <option>contained_by</option> <option>less_than</option> <option>less_than_or_equals</option> <option>greater_than</option> <option>greater_than_or_equals</option> <option>not_equals</option> <option>string_equals</option> <option>length_equals</option> <option>length_greater_than</option> <option>length_greater_than_or_equals</option> <option>length_less_than</option> <option>length_less_than_or_equals</option></select>";

    var myNewRow = tabObj.insertRow(rowsNum);
    var newTdObj0 = myNewRow.insertCell(0);
    var newTdObj1 = myNewRow.insertCell(1);
    var newTdObj2 = myNewRow.insertCell(2);


    newTdObj0.innerHTML = cell_check
    newTdObj1.innerHTML = cell_key;
    if (id === 'variables' || id === 'data') {
        var newTdObj3 = myNewRow.insertCell(3);
        newTdObj2.innerHTML = cell_type;
        newTdObj3.innerHTML = cell_value;
    } else if (id === 'validate') {
        var newTdObj3 = myNewRow.insertCell(3);
        newTdObj2.innerHTML = cell_comparator;
        newTdObj3.innerHTML = cell_type;
        var newTdObj4 = myNewRow.insertCell(4);
        newTdObj4.innerHTML = cell_value;
    } else {
        newTdObj2.innerHTML = cell_value;
    }
}

function add_params(id) {
    var tabObj = document.getElementById(id);//获取添加数据的表格
    var rowsNum = tabObj.rows.length;  //获取当前行数
    var style = 'width:100%; border: none';
    var check = "<input type='checkbox' name='" + id + "' style='width:55px' />";
    var placeholder = '单个:["value1", "value2],  多个:[["name1", "pwd1"],["name2","pwd2"]]';
    var key = "<textarea  name='test[][key]'  placeholder='单个:key, 多个:key1-key2'  style='" + style + "' />";
    var value = "<textarea  name='test[][value]'  placeholder='" + placeholder + "' style='" + style + "' />";
    var myNewRow = tabObj.insertRow(rowsNum);
    var newTdObj0 = myNewRow.insertCell(0);
    var newTdObj1 = myNewRow.insertCell(1);
    var newTdObj2 = myNewRow.insertCell(2);
    newTdObj0.innerHTML = check;
    newTdObj1.innerHTML = key;
    newTdObj2.innerHTML = value;
}

function show_module(module_info, id) {
    module_info = module_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < module_info.length; i++) {
        if (module_info[i] !== "") {
            var value = module_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='请选择' selected>请选择</option>");

}

function auto_load(id, url, target, type) {
    var data = $(id).serializeJSON();
    if (id === '#belong_message' || id === '#form_message') {
        data = {
            "case": {
                "name": data,
                "type": type
            }
        }
    }
    if (id ==='#project') {
        data = {
            "crontab": {
                "name": data,
                "type": type
            }
        }
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
        
                show_module(data, target)
        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function case_ajax(type, editor) {
    var url = $("#url").serializeJSON();
    var method = $("#method").serializeJSON();
    var dataType = $("#DataType").serializeJSON();
    var caseInfo = $("#form_message").serializeJSON();
    var variables = $("#form_variables").serializeJSON();
    var request_data = null;
    if (dataType.DataType === 'json') {
        try {
            request_data  = eval('(' + editor.session.getValue() + ')');
        }
        catch (err) {
            myAlert('Json格式输入有误！');
            return
        }
    } else {
        request_data = $("#form_request_data").serializeJSON();
    }
    var headers = $("#form_request_headers").serializeJSON();
    var extract = $("#form_extract").serializeJSON();
    var validate = $("#form_validate").serializeJSON();
    var parameters = $('#form_params').serializeJSON();
    var hooks = $('#form_hooks').serializeJSON();
    var include = [];
    var i = 0;
    $("ul#pre_case li a").each(function () {
        include[i++] = [$(this).attr('id'), $(this).text()];
    });
    caseInfo['include'] = include;
    const test = {
        "test": {
            "name": caseInfo,
            "parameters": parameters,
            "variables": variables,
            "request": {
                "url": url.url,
                "method": method.method,
                "headers": headers,
                "type": dataType.DataType,
                "request_data": request_data
            },
            "extract": extract,
            "validate": validate,
            "hooks": hooks,
        }
    };
    if (type === 'edit') {
        url = '#';
    } else {
        url = '/httpapitest/case/add';
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(test),
        contentType: "application/json",
        success: function (data) {
           
                if (data.indexOf('/httpapitest/') != -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}
```

在urls.py 中添加
```python
    path('module/search/ajax', views.module_search_ajax, name='module_search_ajax'),
    path('case/add', views.case_add, name='case_add'),
    path('case/search/ajax', views.case_search_ajax, name='case_search_ajax'),
    path('case/edit/<int:id>', views.case_edit, name='case_edit'),
    path('case/list', views.case_list, name='case_list'),
    path('case/delete', views.case_delete, name='case_delete'),
    path('case/copy', views.case_copy, name='case_copy'),
    
```
测试添加case功能
返回报错`The view httpapitest.views.case_list didn't return an HttpResponse object. It returned None instead.`
需要我们实现case_list


###  用例列表 

更新case_list 视图

```python
@csrf_exempt
def case_list(request):
    if request.method == 'GET':
        case = request.GET.get('name','')
        if case:
            rs = TestCase.objects.filter(name__contains=case).order_by("-update_time")
        else:
            rs = TestCase.objects.all().order_by("-update_time")
        info = {'case':case}        
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        context_dict = {'case': objects, 'info':info,}
        return render(request,"case_list.html",context_dict)
```


添加模板case_list.html
```html
{% extends "base.html" %}
{% block title %}用例信息{% endblock %}
{% load staticfiles %}
{% load custom_tags %}
{% block content %}

    <div class="am-modal am-modal-prompt" tabindex="-1" id="my-copy">
        <div class="am-modal-dialog">
            <div style="font-size: medium;" class="am-modal-hd">HAT</div>
            <div class="am-modal-bd">
                <form class="form-horizontal" id="copy_list">
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="index"
                               style="font-weight: inherit; font-size: small " hidden>索引值:</label>
                        <div class="col-sm-9">
                            <input name="index" type="text" class="form-control" id="index"
                                   placeholder="索引值" value="" hidden>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="control-label col-sm-3" for="name"
                               style="font-weight: inherit; font-size: small ">用例名称:</label>
                        <div class="col-sm-9">
                            <input name="name" type="text" class="form-control" id="name"
                                   placeholder="给用例起个名吧" value="">
                        </div>
                    </div>

                </form>
            </div>
            <div class="am-modal-footer">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>提交</span>
            </div>
        </div>
    </div>
    <div class="am-modal am-modal-confirm" tabindex="-1" id="my-invalid">
        <div class="am-modal-dialog">
            <div class="am-modal-hd">HAT</div>
            <div class="am-modal-bd">
                亲，请确认该用例是否被其他用例依赖后再谨慎删除哦
            </div>
            <div class="am-modal-footer">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>确定</span>
            </div>
        </div>
    </div>

    <div class="admin-biaogelist">
        <div class="listbiaoti am-cf">
            <ul class="am-icon-flag on"> 用例列表</ul>
            <dl class="am-icon-home" style="float: right;"> 当前位置： 用例管理 > <a href="#">用例展示</a></dl>
            <dl>
                <button type="button" class="am-btn am-btn-primary am-round am-btn-xs am-icon-plus"
                        onclick="location='{% url 'case_add' %}'">新增用例
                </button>
                <button type="button" class="am-btn am-btn-danger am-round am-btn-xs am-icon-bug"
                        onclick="my_submit()">运行
                </button>
            </dl>
        </div>

        <div class="am-btn-toolbars am-btn-toolbar am-kg am-cf">
            <form id="pro_filter">
                <ul>
                    <li style="padding-top: 5px"><input value="{{ info.name }}" type="text" name="name"
                                                        class="am-input-sm am-input-xm"
                                                        placeholder="用例名称"/>
                    </li>
                    <li>
                        <button style="padding-top: 5px; margin-top: 9px"
                                class="am-btn am-radius am-btn-xs am-btn-success">搜索
                        </button>
                    </li>
                </ul>
            </form>
        </div>


        <form class="am-form am-g" id='test_list' name="test_list">
            <table width="100%" class="am-table am-table-bordered am-table-radius am-table-striped">
                <thead>
                <tr class="am-success">
                    <th class="table-check"><input type="checkbox" id="select_all"/></th>
                    <th class="table-title">序号</th>
                    <th class="table-type">名称</th>
                    <th class="table-type">所属项目</th>
                    <th class="table-type">所属模块</th>
                    <th class="table-type">创建者</th>
                    <th width="163px" class="table-title">操作</th>
                </tr>
                </thead>
                <tbody>
                {% for foo in case %}
                    <tr>
                        <td><input type="checkbox" name="testcase_{{ foo.id }}" value="{{ foo.id }}"/></td>
                        <td>{{ forloop.counter }}</td>
                        <td>
                            {% if foo.include != '[]' %}
                                <div style="float: left">
                                    <a id="co{{ foo.id }}" class="am-icon-plus-square-o am-icon-fw"
                                       style="display: block; cursor: pointer"
                                       onclick="coolspo({{ foo.id }})"></a>
                                    <a id="cc{{ foo.id }}" class="am-icon-minus-square-o am-icon-fw"
                                       style="display: none; cursor: pointer"
                                       onclick="coolspc({{ foo.id }})"></a>
                                </div>

                            {% endif %}

                            <div style="float: left">
                                <a href="{% url 'case_edit' foo.id %}"
                                   data-am-collapse="{target: '#pre_case{{ foo.id }}'}">{{ foo.name }}</a>
                                <nav>
                                    <ul id="pre_case{{ foo.id }}" class="am-nav am-collapse">
                                        {% for path in foo.include|convert_eval %}
                                            {% if path|data_type != 'list' %}
                                                {% if path.config.1|is_del == True %}
                                                    <li id="{{ path.0 }}">
                                                        <span style="color: red;">{{ path.config.1 }}</span>
                                                    </li>
                                                {% else %}
                                                    <li id="{{ path.0 }}">
                                                        <a href="{% url 'config_edit' path.config.0 %}"
                                                           id="{{ path.config.0 }}"
                                                           style="color:cadetblue">{{ path.config.1 }}</a>
                                                    </li>
                                                {% endif %}

                                            {% else %}
                                                {% if path.1|is_del == True %}
                                                    <li id="{{ path.0 }}" s>
                                                       <span style="color: red;">{{ path.1 }}</span>
                                                    </li>
                                                {% else %}
                                                    <li id="{{ path.0 }}">
                                                        <a href="{% url 'case_edit' path.0 %}" id="{{ path.0 }}"
                                                           style="color:rosybrown">{{ path.1 }}</a>
                                                    </li>

                                                {% endif %}

                                            {% endif %}
                                        {% endfor %}
                                    </ul>
                                </nav>
                            </div>
                        </td>
                        <td>{{ foo.belong_project }}</td>
                        <td>{{ foo.belong_module.module_name }}</td>
                        <td>{{ foo.author }}</td>
                        <td>
                            <div class="am-btn-toolbar">
                                <div class="am-btn-group am-btn-group-xs">
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-secondary am-round"
                                            data-am-popover="{content: '运行', trigger: 'hover focus'}"
                                            onclick="run_test('{{ foo.id }}')">
                                        <span class="am-icon-bug"></span>
                                    </button>
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-danger am-round"
                                            data-am-popover="{content: '复制', trigger: 'hover focus'}"
                                            onclick="copy('#copy_list', '{{ foo.id }}')"><span
                                            class="am-icon-copy"></span></button>
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-danger am-round"
                                            data-am-popover="{content: '删除', trigger: 'hover focus'}"
                                            onclick="invalid('{{ foo.id }}')"><span
                                            class="am-icon-trash-o"></span></button>
                                </div>
                            </div>
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>

            <div class="am-btn-group am-btn-group-xs">
                <button type="button" class="am-btn am-btn-default" onclick="location='{% url 'case_add' %}'"><span
                        class="am-icon-plus"></span> 新增用例
                </button>
            </div>

            <ul class="am-pagination am-fr">
                 <span class="step-links">
                                {% if case.has_previous %}
                                   
                                    <a href="#" id='prepage' onclick="previous()">上一页</a>
                                {% endif %}
                        
                                <span class="current">
                                     {{ case.number }}/{{ case.paginator.num_pages }} 页.
                                </span>
                        
                                {% if case.has_next %}
                                
                                   <a href="#" id='nextpage' onclick="next()"> 下一页</a>
                                    
                                {% endif %}
                            </span>
            </ul>


            <hr/>

        </form>
    </div>
    <script type="text/javascript">

        function coolspo(id) {
            $('#co' + id).css('display', 'none');
            $('#cc' + id).css('display', 'block');
            $('#pre_case' + id).collapse('open');
        }

        function coolspc(id) {
            $('#co' + id).css('display', 'block');
            $('#cc' + id).css('display', 'none');
            $('#pre_case' + id).collapse('close');
        }

        function my_submit() {
            if ($("input:checked").size() == 0) {
                myAlert("请至少选择一条用例运行！");
            } else {
                            var data = $("#test_list").serializeJSON();
                            var json2map = JSON.stringify(data);
                            var obj = JSON.parse(json2map);
                            post('#', obj)
            }
        }

        function invalid(name) {
            $('#my-invalid').modal({
                relatedTarget: this,
                onConfirm: function () {
                    del_data_ajax(name, '{% url 'case_delete' %}')
                },
                onCancel: function () {
                }
            });
        }

        function copy(id, index) {
            $('#index').val(index);
            $('#my-copy').modal({
                relatedTarget: this,
                onConfirm: function () {
                    copy_data_ajax(id, '{% url 'case_copy' %}')
                },
                onCancel: function () {
                }
            });
        }

        function run_test(index) {
            post('#', {'id': index})
              
        }

        $('#select_all').click(function () {
            var isChecked = $(this).prop("checked");
            $("input[name^='testcase']").prop("checked", isChecked);
        });

        {% if case.has_next %}
        function next(){
           var params = $("#pro_filter").serialize() + "&page={{ case.next_page_number }}";
           url = "{% url 'case_list' %}" + "?" + params
           $("#nextpage").attr('href',url); 
        }
        {% endif %}
        {% if case.has_previous%}
        function previous(){
            var params = $("#pro_filter").serialize() + "&page={{ case.previous_page_number }}";
           url = "{% url 'case_list' %}" + "?" + params
           $("#prepage").attr('href',url); 
        }
        {% endif %}

    </script>
{% endblock %}
```

这里使用到django模板的高级用法，[自定义模板的过滤器](https://docs.djangoproject.com/zh-hans/2.2/howto/custom-template-tags/)
在httapitest目录下创建一个templatetags包
创建文件 custom_tags.py
```python
import json

from django import template
from httpapitest.utils import update_include

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
```




###  编辑功能

1. 更新case_edit 视图
```
@csrf_exempt
def case_edit(request, id):
    if request.method == 'GET':
        case = TestCase.objects.get(id=id)
        case_request = eval(case.request)
        case_include = eval(case.include)
        context_dict = {
            'project': Project.objects.all().values('project_name').order_by('-create_time'),
            'info': case,
            'request': case_request['test'],
            'include': case_include
        }
        return render(request, 'case_edit.html', context_dict)

    if request.is_ajax():
        case_list = json.loads(request.body.decode('utf-8'))
        msg = case_logic(type=False, **case_list)
        if msg == 'ok':
            return HttpResponse(reverse('case_list'))
        else:
            return HttpResponse(msg)


```
2. 添加case_edit.html模板
```html
{% extends "base.html" %}
{% block title %}修改用例{% endblock %}
{% load staticfiles %}
{% load custom_tags %}

{% block content %}

    <div class="am-modal am-modal-confirm" tabindex="-1" id="save_test">
        <div class="am-modal-dialog">
            <div class="am-modal-hd">HAT</div>
            <form class="form-horizontal" id="form_message">
                <div class="form-group" style="display: none">
                    <label class="control-label col-sm-3" for="test_index"
                           style="font-weight: inherit; font-size: small ">用例索引:</label>
                    <div class="col-sm-8">
                        <input name="test_index" type="text" class="form-control" id="test_index"
                               placeholder="模块名称" value="{{ info.id }}">
                    </div>
                </div>

                <div class="form-group" style="display: none">
                    <label class="control-label col-sm-3" for="author"
                           style="font-weight: inherit; font-size: small ">编写人员:</label>
                    <div class="col-sm-8">
                        <input name="author" type="text" class="form-control" id="author"
                               placeholder="模块名称" value="{{ info.author }}">
                    </div>
                </div>


                <div class="form-group">
                    <label class="control-label col-sm-3" for="case_name"
                           style="font-weight: inherit; font-size: small ">用例名称:</label>
                    <div class="col-sm-8">
                        <input name="case_name" type="text" class="form-control" id="case_name"
                               placeholder="给用例起个名吧" value="{{ info.name }}">
                    </div>
                </div>

                <div class="form-group">
                    <label class="control-label col-sm-3"
                           style="font-weight: inherit; font-size: small ">选择项目:</label>
                    <div class="col-sm-8">
                        <select name="project" class="form-control"
                                onchange="auto_load('#form_message', '{%  url 'module_search_ajax' %}', '#module', 'module')">
                            <option value="{{ info.belong_project }}"
                                    selected>{{ info.belong_project }}</option>
                            {% for obj in project %}
                                {% ifnotequal info.belong_project obj.project_name %}
                                    <option value='{{ obj.project_name }}'>{{ obj.project_name }}</option>
                                {% endifnotequal %}
                            {% endfor %}
                            <option value="请选择">请选择</option>
                        </select>
                    </div>

                </div>

                <div class="form-group">
                    <label class="control-label col-sm-3"
                           style="font-weight: inherit; font-size: small ">选择模块:</label>
                    <div class="col-sm-8">
                        <select class="form-control" id="module" name="module">
                            <option value="{{ info.belong_module.id }}">{{ info.belong_module.module_name }}</option>
                        </select>
                    </div>

                </div>
            </form>
            <div class="am-modal-footer">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>确定</span>
            </div>
        </div>
    </div>


    <div class="admin-biaogelist" xmlns="http://www.w3.org/1999/html" xmlns="http://www.w3.org/1999/html">

        <div class="listbiaoti am-cf">
            <ul class="am-icon-flag on"> 用例修改</ul>
            <dl class="am-icon-home" style="float: right;">当前位置： 用例管理 > <a href="#">修改用例</a></dl>
        </div>

        <div class="am-tabs am-margin">
            <ul class="am-tabs-nav am-nav am-nav-tabs" id="tab-test">
                
                <li><a href="javascript:;" data-target="#tab3">请求</a></li>
                <li><a href="javascript:;" data-target="#tab4">提取/验证</a></li>
                <li><a href="javascript:;" data-target="#tab2">变量/hooks</a></li>
                <li><a href="javascript:;" data-target="#tab1">依赖信息</a></li>
            </ul>

            <div class="am-tabs-bd">
                <div class="am-tab-panel" id="tab1">
                    <div style="float: left; width: 40%;">
                        <form class="form-horizontal" id="belong_message">

                            <div class="form-group">
                                <div class="input-group col-md-10 col-md-offset-1">
                                    <div class="input-group-addon" style="color: #0a628f">可选项目</div>
                                    <select name="project" class="form-control"
                                            onchange="auto_load('#belong_message', '{% url 'module_search_ajax' %}', '#belong_module_id', 'module')">
                                        <option value="{{ info.belong_project }}"
                                                selected>{{ info.belong_project }}</option>
                                        {% for obj in project %}
                                            {% ifnotequal info.belong_project obj.project_name %}
                                                <option value='{{ obj.project_name }}'>{{ obj.project_name }}</option>
                                            {% endifnotequal %}
                                        {% endfor %}
                                        <option value="请选择">请选择</option>
                                    </select>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="input-group col-md-10 col-md-offset-1">
                                    <div class="input-group-addon" style="color: #0a628f">可选模块</div>
                                    <select id="belong_module_id" name="module" class="form-control"
                                            onchange="auto_load('#belong_message', '{% url 'case_search_ajax' %}', '#belong_case_id', 'case');">
                                        <option value="{{ info.belong_module.id }}">{{ info.belong_module.module_name }}</option>
                                    </select>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="input-group col-md-10 col-md-offset-1">
                                    <div class="input-group-addon" style="color: #0a628f">可选用例</div>
                                    <select id="belong_case_id" name="include" class="form-control">
                                    </select>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div style="float: right; width: 50%;margin-right: 1%;">
                        <div class="form-group">
                            <div class="input-group col-md-10">
                                <div class="input-group-addon" id="close_collapse" style="color: #0a628f">用例列表</div>

                                <a class="am-btn am-btn-primary am-radius am-btn-block" href="#" id="pre_collapse"
                                   style="font-size: 16px; background-color: #fff; color: #555; text-align: left"
                                   data-am-collapse="{target: '#pre_case'}">
                                    用 例 执 行 顺 序
                                </a>
                                <nav>
                                    <ul id="pre_case" class="am-nav">
                                        {% for foo in info.include|convert_eval %}
                                            {% if foo|data_type != 'list' %}
                                                <li id="{{ foo.config.0 }}" name="pre_config">
                                                    <a href="/httpapitest/case/edit/{{ foo.config.0 }}"
                                                       id="{{ foo.config.0 }}"
                                                       style="color:cadetblue">{{ foo.config.1 }}</a>
                                                    <i class="js-remove"
                                                       onclick=remove_self('#{{ foo.config.0 }}')>✖</i></li>
                                                </li>
                                            {% else %}
                                                <li id="{{ foo.0 }}">
                                                    <a href="/httpapitest/case/edit/{{ foo.0 }}"
                                                       id="{{ foo.0 }}">{{ foo.1 }}</a>
                                                    <i class="js-remove" onclick=remove_self('#{{ foo.0 }}')>✖</i>
                                                </li>

                                            {% endif %}
                                        {% endfor %}

                                    </ul>
                                </nav>

                            </div>
                        </div>
                    </div>
                </div>
                <div class="am-tab-panel" id="tab2">
                    <button class="btn btn-info" value="添 加" onclick="add_row('variables')">add variables</button>
                    <button class="btn btn-danger" value="删 除" onclick="del_row('variables')">del variables</button>
                    <button class="btn btn-info" value="添 加" onclick="add_row('hooks')">add hooks</button>
                    <button class="btn btn-danger" value="删 除" onclick="del_row('hooks')">del hooks</button>
                    <form id="form_variables">
                        <table class="table table-hover table-condensed table-bordered table-striped" id="variables">
                            <caption>Variables:</caption>
                            <thead>
                            <tr class="active text-success">
                                <th width="5%" align="center">Option</th>
                                <th width="30%" align="center">Key</th>
                                <th width="8%" align="center">Type</th>
                                <th width="57%" align="center">Value</th>
                            </tr>
                            </thead>
                            <tbody>
                            {% for foo in request.variables %}
                                <tr>
                                    <td><input type="checkbox" name="variables" style="width:55px"></td>
                                    {% for key, value in foo.items %}

                                        <td><input type="text" name="test[][key]"
                                                   value="{{ key }}" style="width:100%; border: none"></td>
                                        <td>
                                            <select name='test[][type]'
                                                    class='form-control'
                                                    style='height: 25px; font-size: 15px; padding-top: 0px; padding-left: 0px; border: none'>

                                                {% if value|data_type == 'str' %}
                                                    <option>string</option>
                                                    <option>int</option>
                                                    <option>float</option>
                                                    <option>boolean</option>
                                                {% elif value|data_type == 'int' %}
                                                    <option>int</option>
                                                    <option>string</option>
                                                    <option>float</option>
                                                    <option>boolean</option>
                                                {% elif value|data_type == 'float' %}
                                                    <option>float</option>
                                                    <option>string</option>
                                                    <option>int</option>
                                                    <option>boolean</option>
                                                {% elif value|data_type == 'bool' %}
                                                    <option>boolean</option>
                                                    <option>string</option>
                                                    <option>int</option>
                                                    <option>float</option>
                                                {% endif %}
                                            </select>
                                        </td>
                                        <td><input type="text"
                                                   name="test[][value]" value="{{ value }}"
                                                   style="width:100%; border: none"></td>
                                    {% endfor %}
                                </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </form>

                    
                    <form id="form_hooks">
                        <table class="table table-hover table-condensed table-bordered table-striped" id="hooks">
                            <caption>hooks:</caption>
                            <thead>
                            <tr class="active text-success">
                                <th width="5%" align="center">Option</th>
                                <th width="47.5%" align="center">setup_hooks</th>
                                <th width="47.5%" align="center">teardown_hooks</th>
                            </tr>
                            </thead>
                            <tbody>
                            {% if request.setup_hooks|length >= request.teardown_hooks|length %}
                                {% for foo in  request.setup_hooks %}
                                    <tr>
                                        <td><input type="checkbox" name="hooks" style="width:55px"></td>
                                        <td><input type="text" name='test[][key]'
                                                   value="{{ foo }}" style="width:100%; border: none"></td>
                                        <td>
                                            {% for foos in  request.teardown_hooks %}
                                                {% if forloop.parentloop.counter0 == forloop.counter0 %}
                                                    <input type="text" name='test[][value]'
                                                           value="{{ foos }}"
                                                           style="width:100%; border: none">
                                                {% endif %}
                                            {% endfor %}
                                            {% if forloop.counter > request.teardown_hooks|length %}
                                                <input type="text" name='test[][value]'
                                                       value=""
                                                       style="width:100%; border: none">

                                            {% endif %}
                                        </td>

                                    </tr>
                                {% endfor %}
                            {% else %}
                                {% for foo in  request.teardown_hooks %}
                                    <tr>
                                        <td><input type="checkbox" name="hooks" style="width:55px"></td>
                                        <td>
                                            {% for foos in  request.setup_hooks %}
                                                {% if forloop.parentloop.counter0 == forloop.counter0 %}
                                                    <input type="text" name='test[][key]'
                                                           value="{{ foos }}"
                                                           style="width:100%; border: none">
                                                {% endif %}
                                            {% endfor %}
                                            {% if forloop.counter > request.setup_hooks|length %}
                                                <input type="text" name='test[][key]'
                                                       value=""
                                                       style="width:100%; border: none">

                                            {% endif %}
                                        </td>
                                        <td><input type="text" name='test[][value]'
                                                   value="{{ foo }}" style="width:100%; border: none"></td>

                                    </tr>
                                {% endfor %}

                            {% endif %}

                            </tbody>
                        </table>
                    </form>

                </div>
                <div class="am-tab-panel" id="tab3">
                    <div class="form-inline">
                        <div class="form-group">
                            <div class="input-group">
                                <div class="input-group-addon">URL</div>
                                <input type="text" class="form-control am-input-sm " placeholder="api url"
                                       name="url"
                                       id="url" value="{{ request.request.url }}">
                            </div>
                        </div>

                        <div class="form-group">
                            <div class="input-group">
                                <div class="input-group-addon">Method</div>
                                <select class="form-control" name="method" id="method">
                                    <option>{{ request.request.method }}</option>
                                    {% if request.request.method == 'GET' %}
                                        <option>POST</option>
                                        <option>PUT</option>
                                        <option>DELETE</option>
                                    {% elif request.request.method == 'POST' %}
                                        <option>GET</option>
                                        <option>PUT</option>
                                        <option>DELETE</option>
                                    {% elif request.request.method == 'PUT' %}
                                        <option>GET</option>
                                        <option>POST</option>
                                        <option>DELETE</option>
                                    {% elif request.request.method == 'DELETE' %}
                                        <option>GET</option>
                                        <option>POST</option>
                                        <option>DELETE</option>

                                    {% endif %}
                                </select>
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="input-group">
                                <div class="input-group-addon">Type</div>
                                <select class="form-control" name="DataType" id="DataType">
                                    {% if 'data' in request.request.keys %}
                                        <option selected>data</option>
                                        <option>json</option>
                                        <option>params</option>
                                    {% elif 'json' in request.request.keys %}
                                        <option selected>json</option>
                                        <option>data</option>
                                        <option>params</option>
                                    {% elif 'params' in request.request.keys %}
                                        <option selected>params</option>
                                        <option>data</option>
                                        <option>json</option>
                                    {% else %}
                                        <option>data</option>
                                        <option>json</option>
                                        <option>params</option>

                                    {% endif %}
                                </select>
                            </div>
                        </div>

                        <button class="btn btn-info" value="添 加" onclick="add_row('data')" id="add_data">add data
                        </button>
                        <button class="btn btn-danger" value="删 除" onclick="del_row('data')" id="del_data">del data
                        </button>
                        <button class="btn btn-info" value="添 加" onclick="add_row('header')">add headers</button>
                        <button class="btn btn-danger" value="删 除" onclick="del_row('header')">del headers</button>
                        <form id="form_request_data">
                            {% if 'json' in request.request.keys %}
                                <span style="font-size:10px;" id="json-text">
                                   <div style="margin-left: 0px; margin-top: 5px; height: 200px">
                                       <pre id="code" class="ace_editor"
                                            style="margin-top: 0px; margin-bottom: 0px; min-height: 200px;">
<textarea style="left: 0px">
{{ request.request.json|json_dumps }}
</textarea>
                                       </pre>
                                   </div>
                                </span>
                            {% else %}
                                <table class="table table-hover table-condensed table-bordered table-striped" id="data">
                                    <caption>request:</caption>
                                    <thead>
                                    <tr class="active text-success">
                                        <th width="5%" align="center">Option</th>
                                        <th width="30%" align="center">Key</th>
                                        <th width="5%" align="center">Type</th>
                                        <th width="60%" align="center">Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {% if 'data' in request.request.keys %}
                                        {% for key, value in request.request.data.items %}
                                            <tr>
                                                <td><input type="checkbox" name="data" style="width:55px">
                                                </td>
                                                <td><input type="text" name='test[][key]' value="{{ key }}"
                                                           style="width:100%; border: none"></td>
                                                <td><select name='test[][type]'
                                                            class='form-control'
                                                            style='height: 25px; font-size: 15px; padding-top: 0px; padding-left: 0px; border: none'>
                                                    {% if value|data_type == 'str' %}
                                                        <option>string</option>
                                                        <option>int</option>
                                                        <option>float</option>
                                                        <option>boolean</option>
                                                    {% elif value|data_type == 'int' %}
                                                        <option>int</option>
                                                        <option>string</option>
                                                        <option>float</option>
                                                        <option>boolean</option>
                                                    {% elif value|data_type == 'float' %}
                                                        <option>float</option>
                                                        <option>string</option>
                                                        <option>int</option>
                                                        <option>boolean</option>
                                                    {% elif value|data_type == 'bool' %}
                                                        <option>boolean</option>
                                                        <option>string</option>
                                                        <option>int</option>
                                                        <option>float</option>
                                                    {% endif %}
                                                </select></td>
                                                <td><input type="text" name='test[][value]' value="{{ value }}"
                                                           style="width:100%; border: none"></td>
                                            </tr>
                                        {% endfor %}
                                    {% elif 'params' in request.request.keys %}
                                        {% for key, value in request.request.params.items %}
                                            <tr>
                                                <td><input type="checkbox" name="data"
                                                           style="width:55px">
                                                </td>
                                                <td><input type="text" name='test[][key]' value="{{ key }}"
                                                           style="width:100%; border: none"></td>
                                                <td><select name='test[][type]'
                                                            class='form-control'
                                                            style='height: 25px; font-size: 15px; padding-top: 0px; padding-left: 0px; border: none'>
                                                    {% if value|data_type == 'str' %}
                                                        <option>string</option>
                                                        <option>int</option>
                                                        <option>float</option>
                                                        <option>boolean</option>
                                                    {% elif value|data_type == 'int' %}
                                                        <option>int</option>
                                                        <option>string</option>
                                                        <option>float</option>
                                                        <option>boolean</option>
                                                    {% elif value|data_type == 'float' %}
                                                        <option>float</option>
                                                        <option>string</option>
                                                        <option>int</option>
                                                        <option>boolean</option>
                                                    {% elif value|data_type == 'bool' %}
                                                        <option>boolean</option>
                                                        <option>string</option>
                                                        <option>int</option>
                                                        <option>float</option>
                                                    {% endif %}
                                                </select></td>
                                                <td><input type="text" name='test[][value]' value="{{ value }}"
                                                           style="width:100%; border: none"></td>
                                            </tr>
                                        {% endfor %}
                                    {% endif %}
                                    </tbody>
                                </table>
                            {% endif %}
                        </form>

                        <form id="form_request_headers">
                            <table class="table table-hover table-condensed table-bordered table-striped" id="header">
                                <caption>headers:</caption>
                                <thead>
                                <tr class="active text-success">
                                    <th width="5%" align="center">Option</th>
                                    <th width="40%" align="center">Key</th>
                                    <th width="55%" align="center">Value</th>
                                </tr>
                                </thead>
                                <tbody>
                                {% if 'headers' in request.request.keys %}
                                    {% for key, value in request.request.headers.items %}
                                        <tr>
                                            <td><input type="checkbox" name="header" style="width:55px">
                                            </td>
                                            <td><input type="text" name='test[][key]' value="{{ key }}"
                                                       style="width:100%; border: none"></td>
                                            <td><input type="text" name='test[][value]' value="{{ value }}"
                                                       style="width:100%; border: none"></td>
                                        </tr>
                                    {% endfor %}
                                {% endif %}
                                </tbody>
                            </table>
                        </form>
                    </div>
                </div>
                <div class="am-tab-panel" id="tab4">
                    <button class="btn btn-info" value="添 加" onclick="add_row('extract')">add extract</button>
                    <button class="btn btn-danger" value="删 除" onclick="del_row('extract')">del extract</button>
                    <button class="btn btn-info" value="添 加" onclick="add_row('validate')">add validate</button>
                    <button class="btn btn-danger" value="删 除" onclick="del_row('validate')">del validate</button>
                    <form id="form_extract">
                        <table class="table table-hover table-condensed table-bordered table-striped" id="extract">
                            <caption>extract:</caption>
                            <thead>
                            <tr class="active text-success">
                                <th width="5%" align="center">Option</th>
                                <th width="40%" align="center">Key</th>
                                <th width="55%" align="center">Value</th>
                            </tr>
                            </thead>
                            <tbody>
                            {% for foo in request.extract %}
                                <tr>
                                    <td><input type="checkbox" name="extract" style="width:55px"></td>
                                    {% for key, value in foo.items %}

                                        <td><input type="text" name='test[][key]' value="{{ key }}"
                                                   style="width:100%; border: none"></td>
                                        <td><input type="text" name='test[][value]' value="{{ value }}"
                                                   style="width:100%; border: none"></td>
                                    {% endfor %}
                                </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </form>
                    <form id="form_validate">
                        <table class="table table-hover table-condensed table-bordered table-striped" id="validate">
                            <caption>validate:</caption>
                            <thead>
                            <tr class="active text-success">
                                <th width="2%" align="center">Option</th>
                                <th width="30%" align="center">Check</th>
                                <th width="10%" align="center">Comparator</th>
                                <th width="8%" align="center">Type</th>
                                <th width="50%" align="center">Expected</th>
                            </tr>
                            </thead>
                            <tbody>
                            {% for foo in request.validate %}
                                <tr>
                                    <td><input type="checkbox" name="validate"
                                               style="width:55px"></td>
                                    <td><input type="text" name='test[][key]' value="{{ foo.check }}"
                                               style="width:100%; border: none"></td>
                                    <td><select name='test[][comparator]' class="form-control"
                                                style="height: 25px; font-size: 15px; padding-top: 0px; padding-left: 0px; border: none">
                                        {% ifequal foo.comparator 'equals' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>equals</option>
                                        {% endifequal %}

                                        {% ifequal foo.comparator 'contains' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>contains</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'startswith' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>startswith</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'endswith' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>endswith</option>
                                        {% endifequal %}

                                        {% ifequal foo.comparator 'regex_match' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>regex_match</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'type_match' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>type_match</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'contained_by' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>contained_by</option>
                                        {% endifequal %}

                                        {% ifequal foo.comparator 'less_than' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>less_than</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'less_than_or_equals' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>less_than_or_equals</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'greater_than' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>greater_than</option>
                                        {% endifequal %}

                                        {% ifequal foo.comparator 'greater_than_or_equals' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>greater_than_or_equals</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'not_equals' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>not_equals</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'string_equals' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>string_equals</option>
                                        {% endifequal %}

                                        {% ifequal foo.comparator 'length_equals' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>length_equals</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'length_greater_than' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>length_greater_than</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'length_greater_than_or_equals' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>length_greater_than_or_equals</option>
                                        {% endifequal %}

                                        {% ifequal foo.comparator 'length_less_than' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>length_less_than</option>
                                        {% endifequal %}
                                        {% ifequal foo.comparator 'length_less_than_or_equals' %}
                                            <option selected>{{ foo.comparator }}</option>
                                        {% else %}
                                            <option>length_less_than_or_equals</option>
                                        {% endifequal %}

                                    </select></td>
                                    <td>
                                        <select name='test[][type]'
                                                class='form-control'
                                                style='height: 25px; font-size: 15px; padding-top: 0px; padding-left: 0px; border: none'>
                                            {% if foo.expect|data_type == 'str' %}
                                                <option>string</option>
                                                <option>int</option>
                                                <option>float</option>
                                                <option>boolean</option>
                                            {% elif foo.expect|data_type == 'int' %}
                                                <option>int</option>
                                                <option>string</option>
                                                <option>float</option>
                                                <option>boolean</option>
                                            {% elif foo.expect|data_type == 'float' %}
                                                <option>float</option>
                                                <option>string</option>
                                                <option>int</option>
                                                <option>boolean</option>
                                            {% elif foo.expect|data_type == 'bool' %}
                                                <option>boolean</option>
                                                <option>string</option>
                                                <option>int</option>
                                                <option>float</option>
                                            {% endif %}
                                        </select>
                                    </td>
                                    <td><input type="text" name='test[][value]' value="{{ foo.expect }}"
                                               style="width:100%; border: none"></td>
                                </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </form>
                </div>

            </div>

        </div>

        <div class="am-form-group am-cf">
            <div class="you" style="margin-left: 11%;">
                <button type="button" id="save" class="am-btn am-btn-success am-radius">点 击 修
                    改
                </button>&nbsp;
                &raquo; &nbsp;
                <a type="submit" href="{% url 'case_add' %}" class="am-btn am-btn-secondary am-radius">新 增 用 例</a>
            </div>
        </div>
    </div>

    <script>
        try {
            editor = ace.edit("code");
            init_acs('json', 'github', editor);
        } catch (err) {
            editor = null;
        }
        $('#DataType').on('change', function () {
            if ($('#DataType').val() === 'json') {
                $('#add_data').attr('disabled', true);
                $('#del_data').attr('disabled', true);
                $('#data').remove();
                var json_text = "<span style=\"font-size:10px;\" id=\"json-text\">\n" +
                    " <div style=\"margin-left: 0px; margin-top: 5px; height: 200px\">" +
                    "<pre id=\"code\" class=\"ace_editor\" style=\"margin-top: 0px; margin-bottom: 0px; min-height: 200px;\">\n" +
                    "<textarea>\n" +
                    "{\"key\":\"value\"}\n" +
                    "</textarea>\n" +
                    "</pre></div></span>";
                $('#form_request_data').append(json_text);
                editor = ace.edit("code");
                init_acs('json', 'github', editor);

            } else {
                var table = '<table class="table table-hover table-condensed table-bordered table-striped" id="data">\n' +
                    '                                <caption>' + $('#DataType').val() + ':</caption>\n' +
                    '                                <thead>\n' +
                    '                                <tr class="active text-success">\n' +
                    '                                    <th width="5%" align="center">Option</th>\n' +
                    '                                    <th width="30%" align="center">Key</th>\n' +
                    '                                    <th width="5%" align="center">Type</th>\n' +
                    '                                    <th width="60%" align="center">Value</th>\n' +
                    '                                </tr>\n' +
                    '                                </thead>\n' +
                    '                                <tbody>\n' +
                    '                                </tbody>\n' +
                    '                            </table>';

                $('#add_data').text('add ' + $('#DataType').val());
                $('#del_data').text('del ' + $('#DataType').val());

                $('#add_data').removeAttr("disabled");
                $('#del_data').removeAttr("disabled");
                $('#data').remove();
                $('#json-text').remove();
                $('#form_request_data').append(table);
            }
        });

        $("#tab-test").on("click", "li", function () {
            $(this).addClass("am-active").siblings("li").removeClass("am-active");
            var target = $(this).children("a").attr("data-target");
            $(target).addClass("am-active").siblings(".am-tab-panel").removeClass("am-active");
        }).find("li").eq(0).trigger("click");

        $(function () {
            $("#pre_case").sortable();
            $("#pre_case").disableSelection();
        });

        $('#belong_case_id').on('change', function () {
            if ($('#belong_case_id').val() !== '请选择') {
                case_id = $('#belong_case_id').val();
                case_name = $('#belong_case_id option:selected').text();
                var href = "<li id=" + case_id + "><a href='/httpapitest/case/edit/" + case_id + "' id = " + case_id + ">" + case_name + "" +
                    "</a><i class=\"js-remove\" onclick=remove_self('#" + case_id + "')>✖</i></li>";
                $("#pre_case").append(href);
            }
        });

        function remove_self(id) {
            $(id).remove();
        }

        $('#config').on('change', function () {
            if ($('#config').val() !== '请选择') {
                var case_id = $('#config').val();
                var case_name = $('#config option:selected').text();
                var href = "<li id=" + case_id + " name='pre_config'><a style='color: cadetblue' href='/httpapitest/config/edit/" + case_id + "' id = " + case_id + ">" + case_name + "" +
                    "</a><i class=\"js-remove\" onclick=remove_self('#" + case_id + "')>✖</i></li>";
                $("li[name='pre_config']").remove();
                $("#pre_case").prepend(href);
                $('#config_pre').val("{'config': ['" + case_id + "', '" + case_name + "']}");
            }
        });

        $(function () {
            $('#add_data').text('add ' + $('#DataType').val());
            $('#del_data').text('del ' + $('#DataType').val());
        });

        $(function () {
            if ($("li[name='pre_config']")) {
                var case_id = $('#config').val();
                var case_name = $('#config option:selected').text();
                $('#config_pre').val("{'config': ['" + case_id + "', '" + case_name + "']}");
            }

        });

        $('#save').on('click', function () {
            if ($("li[name='pre_config']").length <= 0) {
                $('#config_pre').val("");
            }
            $('#save_test').modal({
                relatedTarget: this,
                onConfirm: function () {
                    case_ajax('edit', editor)
                },
                onCancel: function () {
                }
            });
        })

    </script>
{% endblock %}


```
3. custom_tags.py 添加函数
```
@register.filter(name='json_dumps')
def json_dumps(value):
    return json.dumps(value, indent=4, separators=(',', ': '), ensure_ascii=False)
```
测试编辑功能

###  删除功能
修改case_delete视图
```
@csrf_exempt
def case_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        case_id = data.get('id')
        case = TestCase.objects.get(id=case_id)
        case.delete()
        return HttpResponse(reverse('case_list'))
```

测试删除功能

###  拷贝功能
views添加视图函数
```
@csrf_exempt
def case_copy(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        config_id = data['data']['index']
        name = data['data']['name']
        case = TestCase.objects.get(id=config_id)
        belong_module = case.belong_module
        if TestCase.objects.filter(name=name, belong_module=belong_module).count() > 0:
            return HttpResponse("用例名称重复")
        else:
            case.name = name
            case.id = None
            case.save()
            return HttpResponse(reverse('case_list'))
```
commons.js添加 copy_data_ajax函数
```js
function copy_data_ajax(id, url) {
    var data = {
        "data": $(id).serializeJSON(),
        'mode': 'copy'
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data.indexOf('/httpapitest/') !== -1) {
                window.location.href = data;
            } else {
                myAlert(data);
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}
```

测试拷贝功能

修改base.html
```html
            <ul>
                <li><a href="{% url 'case_add' %}">新 增 用 例</a></li>
                <li><a href="{% url 'case_list' %}">用 例 列 表</a></li>
            </ul>
```
