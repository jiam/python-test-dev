# 实战http接口测试平台HAT

## 功能模块
+ dashboard
+ 项目管理
+ 模块管理
+ 用例管理
+ 报告管理
+ 定时任务


## 系统架构

![img](./Chapter-10/pics/arch.jpg)
+ httprunner 接口测试框架
+ redis 缓存队列
+ celery 分布式任务系统

## 数据库表结构

项目表ProjectInfo
| Field            | Type         | Null | Key | Default | Extra          |
|------------------|--------------|------|-----|---------|----------------|
| id               | int(11)      | NO   | PRI | NULL    | auto_increment |
| create_time      | datetime(6)  | NO   |     | NULL    |                |
| update_time      | datetime(6)  | NO   |     | NULL    |                |
| project_name     | varchar(50)  | NO   | UNI | NULL    |                |
| responsible_name | varchar(20)  | NO   |     | NULL    |                |
| test_user        | varchar(100) | NO   |     | NULL    |                |
| dev_user         | varchar(100) | NO   |     | NULL    |                |
| publish_app      | varchar(100) | NO   |     | NULL    |                |
| simple_desc      | varchar(100) | YES  |     | NULL    |                |
| other_desc       | varchar(100) | YES  |     | NULL    |                |

模块表

| Field             | Type         | Null | Key | Default | Extra          |
|-------------------|--------------|------|-----|---------|----------------|
| id                | int(11)      | NO   | PRI | NULL    | auto_increment |
| create_time       | datetime(6)  | NO   |     | NULL    |                |
| update_time       | datetime(6)  | NO   |     | NULL    |                |
| module_name       | varchar(50)  | NO   |     | NULL    |                |
| test_user         | varchar(50)  | NO   |     | NULL    |                |
| simple_desc       | varchar(100) | YES  |     | NULL    |                |
| other_desc        | varchar(100) | YES  |     | NULL    |                |
| belong_project_id | int(11)      | NO   | MUL | NULL    |                |

用例表

| Field            | Type          | Null | Key | Default | Extra          |
|------------------|---------------|------|-----|---------|----------------|
| id               | int(11)       | NO   | PRI | NULL    | auto_increment |
| create_time      | datetime(6)   | NO   |     | NULL    |                |
| update_time      | datetime(6)   | NO   |     | NULL    |                |
| name             | varchar(50)   | NO   |     | NULL    |                |
| belong_project   | varchar(50)   | NO   |     | NULL    |                |
| author           | varchar(20)   | NO   |     | NULL    |                |
| request          | longtext      | NO   |     | NULL    |                |
| belong_module_id | int(11)       | NO   | MUL | NULL    |                |
| include          | varchar(1024) | YES  |     | NULL    |                |

报告表

| Field       | Type        | Null | Key | Default | Extra          |
|-------------|-------------|------|-----|---------|----------------|
| id          | int(11)     | NO   | PRI | NULL    | auto_increment |
| create_time | datetime(6) | NO   |     | NULL    |                |
| update_time | datetime(6) | NO   |     | NULL    |                |
| report_name | varchar(40) | NO   |     | NULL    |                |
| start_at    | varchar(40) | YES  |     | NULL    |                |
| status      | tinyint(1)  | NO   |     | NULL    |                |
| testsRun    | int(11)     | NO   |     | NULL    |                |
| successes   | int(11)     | NO   |     | NULL    |                |
| reports     | longtext    | NO   |     | NULL    |                |

用户表

| Field       | Type         | Null | Key | Default | Extra          |
|-------------|--------------|------|-----|---------|----------------|
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| create_time | datetime(6)  | NO   |     | NULL    |                |
| update_time | datetime(6)  | NO   |     | NULL    |                |
| username    | varchar(20)  | NO   | UNI | NULL    |                |
| password    | varchar(20)  | NO   |     | NULL    |                |
| email       | varchar(254) | NO   | UNI | NULL    |                |
| status      | int(11)      | NO   |     | NULL    |                |


## 新建项目

1. 创建项目 

    `django-admin startproject hat`

2. 创建app

进入hat目录

    `python  manage.py startapp httpapitest`

3. 修改settings.py 添加 httpapitest到 INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'httpapitest',
]
```

4. 启动开发服务器

    `python manage.py runserver`

访问127.0.0.1:8000，显示django界面说明，一切ok

5. 数据库
安装mysql

windows系统在群里下载mysql文件，解压即可
安装python 的mysqlclient 模块；python通过改模块连接mysql数据库

    `pip install --only-binary :all: mysqlclient`
    --only-binary 安装编译好的二进制
mac 系统
```
brew install mysql
brew services start mysql
pip3 install mysqlclient
```
如果没有brew命令,执行以下命令进行安装
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`

创建数据库

```powershell
PS D:\mysql-5.6.42-winx64\bin> .\mysql.exe -uroot -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.6.42 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE DATABASE `hat` /*!40100 DEFAULT CHARACTER SET utf8 */;
Query OK, 1 row affected (0.02 sec)

mysql>
```


6. 配置mysql数据库

修改settings.py
```python
DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hat',  # 新建数据库名
        'USER': 'root',  # 数据库登录名
        'PASSWORD': '',  # 数据库登录密码
        'HOST': '127.0.0.1',  # 数据库所在服务器ip地址
        'PORT': '3306',  # 监听端口 默认3306即可
        }
}
```

7. 配置静态文件路径编辑settings.py文件

```python
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR, ]
```
在manage.py同级目录创建static目录

8. 配置模板路径

```python
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]
```

在manage.py同级目录创建static目录,创建templates目录

9. 配置项目目录下的urls.py 将匹配/httapitest的url 路由到app httpapitest的urls.py
```python
from django.contrib import admin
from django.urls import path, include
from httpapitest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('httpapitest/', include('httpapitest.urls')),
    
]
```
此时runserver会报错，因为没有index视图函数

10. 在httpapitest目录下新建urls.py文件
```python

from django.urls import path
from httpapitest import views

urlpatterns = [
    path('', views.index, name='index'),
    
]
```
此时runserver会报错，因为没有index视图函数

11. 创建第一个视图index

```python
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("hello hat")

```
打开http://127.0.0.1:8000 查看


## 项目管理
实现项目的增删改查功能

### 搭建网站页面架构

在templates目录下创建base.html 模板
```html
<!doctype html>
<html class="no-js" lang="zh-CN">
<head>

    <meta charset="utf-8">
    <title>{% block title %}{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    

    {% load staticfiles %}
    <meta name="apple-mobile-web-app-title" content="HAT"/>
    <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" media="screen"/>
    <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    
    <link rel="stylesheet" href="https://cdn.bootcss.com/amazeui/2.7.2/css/amazeui.min.css"/>
    <link rel="stylesheet" href="{% static 'assets/css/admin.css' %}">
    <link rel="stylesheet" href="{% static 'assets/css/common.css' %}">

    <script src="https://cdn.bootcss.com/amazeui/2.7.2/js/amazeui.min.js"></script>
    <script src="https://cdn.bootcss.com/jquery.serializeJSON/2.9.0/jquery.serializejson.min.js"></script>
    <script src="https://cdn.bootcss.com/ace/1.2.6/ace.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://cdn.bootcss.com/ace/1.2.6/ext-language_tools.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://apps.bdimg.com/libs/jqueryui/1.10.4/jquery-ui.min.js"></script>

    <script src="{% static 'assets/js/app.js' %}"></script>
    <script src="{% static 'assets/js/commons.js' %}"></script>


</head>

<body class="modal-open">
<div class="am-modal am-modal-alert" tabindex="-1" id="my-alert">
    <div class="am-modal-dialog">
        <div class="am-modal-hd">HAT</div>
        <div class="am-modal-bd" id="my-alert_print">
            Sorry，服务器可能开小差啦, 请重试!
        </div>
        <div class="am-modal-footer">
            <span class="am-modal-btn">确定</span>
        </div>
    </div>
</div>


<div class="am-cf admin-main">
    <div class="nav-navicon admin-main admin-sidebar">
        <div class="sideMenu am-icon-dashboard" style="color:#aeb2b7; margin: 10px 0 0 0;"> 欢迎您：{{ request.session.now_account }} &nbsp;&nbsp;<a
                href="#">注 销</a></div>
        <div class="sideMenu">
            {% if  "project" in request.path %}
            <h3 class="am-icon-folder on"><em></em> <a href="#">项目管理</a></h3>
            {% else %}
            <h3 class="am-icon-folder"><em></em> <a href="#">项目管理</a></h3>
            {% endif %}
            <ul>
                <li><a href="#">项 目 列 表</a></li>
                <li><a href="#">新 增 项 目</a></li>
            </ul>
            {% if  "module" in request.path %}
            <h3 class="am-icon-th-list on"><em></em> <a href="#"> 模块管理</a></h3>
            {% else %} 
            <h3 class="am-icon-th-list"><em></em> <a href="#"> 模块管理</a></h3>
            {% endif %}
            <ul>
                <li><a href="#">模 块 列 表</a></li>
                <li><a href="#">新 增 模 块</a></li>
            </ul>
            {% if  "case" in request.path %}
            <h3 class="am-icon-bug on"><em></em> <a href="#">用例管理</a></h3>
            {% else %}
            <h3 class="am-icon-bug"><em></em> <a href="#">用例管理</a></h3>
            {% endif %}
            <ul>
                <li><a href="#">新 增 用 例</a></li>
                <li><a href="#">用 例 列 表</a></li>
            </ul>

            <h3 class="am-icon-soundcloud"><em></em> <a href="#">测试计划</a></h3>
            <ul>
                <li><a href="#">定 时 任 务</a></li>
            </ul>


            <h3 class="am-icon-jsfiddle"><em></em> <a href="#">报告管理</a></h3>
            <ul>
                <li><a href="#">查看报告</a></li>
            </ul>
        </div>
        <!-- sideMenu End -->
    </div>

    <div class="daohang">
        <ul>
            <li>
                <button type="button" class="am-btn am-btn-default am-radius am-btn-xs"
                        onclick="location='{% url 'index' %}'">返回首页
                    <a href="{% url 'index' %}" class="am-close am-close-spin">~</a></button>
            </li>
            <li>
                <button type="button" class="am-btn am-btn-default am-radius am-btn-xs"
                        onclick="location='#'">项目列表<a
                        href="#" class="am-close am-close-spin">~</a>
                </button>
            </li>
            <li>
                <button type="button" class="am-btn am-btn-default am-radius am-btn-xs"
                        onclick="location='#'">模块列表<a
                        href="#" class="am-close am-close-spin">~</a>
                </button>
            </li>
            <li>
                <button type="button" class="am-btn am-btn-default am-radius am-btn-xs"
                        onclick="location='#'">用例列表<a
                        href="#" class="am-close am-close-spin">~</a>
                </button>
            </li>
            <li>
                <button type="button" class="am-btn am-btn-default am-radius am-btn-xs"
                        onclick="location='#'">新增用例<a
                        href="#" class="am-close am-close-spin">~</a>
                </button>
            </li>
            <li>
                <button type="button" class="am-btn am-btn-default am-radius am-btn-xs"
                        onclick="location='#'">新增任务<a
                        href="#" class="am-close am-close-spin">~</a>
                </button>
            </li>

        </ul>
    </div>

    {% block content %}

    {% endblock %}
    <script type="text/javascript">
        $(".sideMenu").slide({
            titCell: "h3", //鼠标触发对象
            targetCell: "ul", //与titCell一一对应，第n个titCell控制第n个targetCell的显示隐藏
            effect: "slideDown", //targetCell下拉效果
            delayTime: 300, //效果时间
            triggerTime: 150, //鼠标延迟触发时间（默认150）
            defaultPlay: true,//默认是否执行效果（默认true）
            returnDefault: false //鼠标从.sideMen移走后返回默认状态（默认false）
        });
    </script>
</div>

</body>
</html>
```

### 创建index.html模板

```
{% extends "base.html" %}
{% block title %}首页{% endblock %}
{% load staticfiles %}
{% block content %}
    <div class="admin">
    <h1> dashboard </h1>

    </div>
{% endblock %}
```

### 添加静态文件

群文件assets.zip 解压 放到static目录下

### 更新index视图
```python
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

```
打开http://127.0.0.1:8000/ 


### 在models.py创建项目相关的modle 类
```python
from django.db import models

# Create your models here.

class BaseTable(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'

class Project(BaseTable):
    class Meta:
        verbose_name = '项目信息'
        db_table = 'Project'

    project_name = models.CharField('项目名称', max_length=50, unique=True, null=False)
    responsible_name = models.CharField('负责人', max_length=20, null=False)
    test_user = models.CharField('测试人员', max_length=100, null=False)
    dev_user = models.CharField('开发人员', max_length=100, null=False)
    publish_app = models.CharField('发布应用', max_length=100, null=False)
    simple_desc = models.CharField('简要描述', max_length=100, null=True)
    other_desc = models.CharField('其他信息', max_length=100, null=True)
```
BaseTable 类里面有两个字段create_time、update_time，这两个字段在其他多个类里也要用到，其它需要这两个字段的类继续BaseTable即可；

执行python manage.py makemigrations
```
python manage.py makemigrations
python manage.py migrate
```
打开http://127.0.0.1:8000/ 


### 定义视图
先定义空视图
```
def project_add(request):
    pass

def project_list(request):
    pass

def project_edit(request):
    pass

def project_delete(request):
    pass

```

### 定义url

```

from django.urls import path
from httpapitest import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/list', views.project_list, name='project_list'),
    path('project/add', views.project_add, name='project_add'),
    path('project/edit', views.project_edit, name='project_edit'),
    path('project/delete', views.project_delete, name='project_delete'),
]
```

### 修改project_add视图
导入
```python
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from httpapitest.models import Project, DebugTalk
```
修改视图函数
```python
@csrf_exempt
def project_add(request):

    # 处理ajax提交的表单
    if request.is_ajax():
        project = json.loads(request.body.decode('utf-8'))
        if project.get('project_name') == '':
            msg = '项目名称不能为空'
            return HttpResponse(msg)
        if project.get('responsible_name') == '':
            msg = '负责人不能为空'
            return HttpResponse(msg)
        if project.get('test_user') == '':
            msg = '测试人员不能为空'
            return HttpResponse(msg)
        if project.get('dev_user') == '':
            msg = '开发人员不能为空'
            return HttpResponse(msg)
        if project.get('publish_app') == '':
            msg = '发布应用不能为空'
            return HttpResponse(msg)
        if Project.objects.filter(project_name=project.get('project_name')):
            msg = "项目已经存在"
            return HttpResponse(msg)
        else:
            p = Project()
            p.project_name = project.get('project_name')
            p.responsible_name = project.get('responsible_name')
            p.test_user = project.get('test_user')
            p.dev_user = project.get('dev_user')
            p.publish_app = project.get('publish_app')
            p.simple_desc = project.get('simple_desc')
            p.other_desc = project.get('other_desc')
            p.save()
            d = DebugTalk()
            d.belong_project = p
            d.save()
            return HttpResponse('添加成功')
    # 显示项目添加页面
    if request.method == 'GET':
        return render(request, 'project_add.html')
```
### 新建project_add.html 模板
templates/project_add.html
```html
{% extends "base.html" %}
{% block title %}新增项目{% endblock %}
{% load staticfiles %}
{% block content %}

    <div class=" admin-content">

        <div class="admin-biaogelist">
            <div class="listbiaoti am-cf">
                <ul class="am-icon-flag on"> 新增项目</ul>
                <dl class="am-icon-home" style="float: right;"> 当前位置： 项目管理&gt;新增项目</a></dl>
            </div>
            <div class="fbneirong">
                <form class="form-horizontal" id="project_add">
                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="project_name">项目名称：</label>
                        <div class="col-md-5">
                            <input type="text" class="form-control" id="project_name"
                                   aria-describedby="inputSuccess3Status" name="project_name" placeholder="请输入项目名称"
                                   value="">
                            <span class="glyphicon glyphicon-th-large form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>
                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="responsible_name">负责人：</label>
                        <div class="col-md-5">
                            <input type="text" class="form-control" id="responsible_name" name="responsible_name"
                                   aria-describedby="inputSuccess3Status" placeholder="请指定项目负责人" value="">
                            <span class="glyphicon glyphicon-user form-control-feedback" aria-hidden="true"></span>
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
                        <label class="control-label col-md-2 text-primary" for="dev_user">开发人员：</label>
                        <div class="col-md-5">
                            <input type="text" class="form-control" id="dev_user" name="dev_user"
                                   aria-describedby="inputSuccess3Status" placeholder="请输入项目参与的研发人员" value="">
                            <span class="glyphicon glyphicon-user form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>

                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="publish_app">发布应用：</label>
                        <div class="col-md-5">
                            <input type="text" class="form-control" id="publish_app" name="publish_app"
                                   aria-describedby="inputSuccess3Status" placeholder="请输入发布的应用" value="">
                            <span class="glyphicon glyphicon-upload form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>

                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="simple_desc">简要描述：</label>
                        <div class="col-md-5">
                            <textarea type="text" rows="3" class="form-control" id="simple_desc" name="simple_desc"
                                      aria-describedby="inputSuccess3Status" placeholder="项目简单概述"></textarea>
                            <span class="glyphicon glyphicon-paperclip form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>

                    <div class="form-group  has-feedback">
                        <label class="control-label col-md-2 text-primary" for="other_desc">其他信息：</label>
                        <div class="col-md-5">
                            <textarea type="text" rows="3" class="form-control" id="other_desc" name="other_desc"
                                      aria-describedby="inputSuccess3Status" placeholder="项目其他相关信息描述"></textarea>
                            <span class="glyphicon glyphicon-paperclip form-control-feedback" aria-hidden="true"></span>
                        </div>
                    </div>
                    <div class="am-form-group am-cf">
                        <div class="you" style="margin-left: 8%;">
                            <button type="button" class="am-btn am-btn-success am-radius" id="send"
                                    onclick="project_add('{% url 'project_add' %}')">点 击 提 交
                            </button>&nbsp;
                            &raquo; &nbsp;
                            <a type="submit" href="#" class="am-btn am-btn-secondary am-radius">新 增 模
                                块</a>

                        </div>
                    </div>
                </form>


            </div>
        </div>
    </div>
{% endblock %}

```

### commons.js文件
static/assets/js/commons.js
```js
/*提示 弹出*/
function myAlert(data) {
    $('#my-alert_print').text(data);
    $('#my-alert').modal({
        relatedTarget: this
    });
}


/*添加项目*/
function project_add(url) {
    // 使用jquery获取表单数据
    var data = $('#project_add').serializeJSON(); 

    // 对表单数据做校验
    if (data.project_name === '' ) {
        myAlert('项目名称不能为空')
        return
    }
    if (data.responsible_name === '') {
        myAlert('负责人不能为空')
        return
    }

    if (data.test_user === '') {
        myAlert('测试人员不能为空')
        return
    }

    if (data.dev_user === '') {
        myAlert('开发人员不能为空')
        return
    }

    if (data.dev_user === '') {
        myAlert('发布应用不能为空')
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
使用浏览器打开http://127.0.0.1:8000/httpapitest/project/add 测试添加项目功能


### 修改project_list视图

```python
@csrf_exempt
def project_list(request):
    if request.method == 'GET':
        all_projects = Project.objects.all().order_by("-update_time")
        project_name = request.GET.get('project','All')
        info = {'belong_project': project_name}
        if project_name != 'All':
            rs = Project.objects.filter(project_name=project_name)
        else:
            rs = all_projects
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        projects = paginator.get_page(page)
        context_dict = {'projects': projects, 'all_projects': all_projects,'info': info}
        return render(request,"project_list.html",context_dict)

```
导入Pagintor
`from django.core.paginator import Paginator`


### 添加project_list.html 模板
```html
{% extends "base.html" %}
{% block title %}项目信息{% endblock %}
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
                                   placeholder="索引值" value="" hidden>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="control-label col-sm-3" for="project_name"
                               style="font-weight: inherit; font-size: small ">项目名称：</label>
                        <div class="col-sm-9">
                            <input name="project_name" type="text" class="form-control" id="project_name"
                                   placeholder="项目名称" value="" readonly>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="control-label col-sm-3" for="responsible_name"
                               style="font-weight: inherit; font-size: small ">负责人：</label>
                        <div class="col-sm-9">
                            <input name="responsible_name" type="text" id="responsible_name" class="form-control"
                                   placeholder="负责人" value="">
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
                        <label class="control-label col-sm-3" for="dev_user"
                               style="font-weight: inherit; font-size: small ">开发人员：</label>
                        <div class="col-sm-9">
                            <input name="dev_user" type="text" id="dev_user" class="form-control"
                                   placeholder="开发人员" value="">
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="control-label col-sm-3" for="publish_app"
                               style="font-weight: inherit; font-size: small ">发布应用：</label>
                        <div class="col-sm-9">
                            <input name="publish_app" type="text" id="publish_app" class="form-control"
                                   placeholder="发布应用" value="">
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
            <div class="am-modal-projectter">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>提交</span>
            </div>
        </div>
    </div>

    <div class="am-modal am-modal-confirm" tabindex="-1" id="delete-tip">
        <div class="am-modal-dialog">
            <div class="am-modal-hd">HAT</div>
            <div class="am-modal-bd">
                亲，此操作会强制删除该项目下所有模块和用例，请谨慎操作！！！
            </div>
            <div class="am-modal-projectter">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>确定</span>
            </div>
        </div>
    </div>   

    <div class="am-modal am-modal-confirm" tabindex="-1" id="runProject">
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
            <div class="am-modal-projectter">
                <span class="am-modal-btn" data-am-modal-cancel>取消</span>
                <span class="am-modal-btn" data-am-modal-confirm>确定</span>
            </div>
        </div>
    </div>



    <div class="admin-biaogelist">
        <div class="listbiaoti am-cf">
            <ul class="am-icon-flag on"> 项目列表</ul>
            <dl class="am-icon-home" style="float: right;"> 当前位置： 项目管理 > 项目列表</a></dl>
            <dl>
                <button type="button" class="am-btn am-btn-danger am-round am-btn-xs am-icon-plus"
                        onclick="location='{% url 'project_add' %}'">新增项目
                </button>
                <button type="button" class="am-btn am-btn-danger am-round am-btn-xs am-icon-bug"
                onclick="#"
                >运行
                </button>
            </dl>
        </div>

        <div class="am-btn-toolbars am-btn-toolbar am-kg am-cf">
            <form id="search">
                <ul>
                    <li style="padding-top: 5px">
                        <select name="project" id="projectselect" class="am-input-zm am-input-xm">
                            <option value="{{ info.belong_project }}"
                                    selected>{{ info.belong_project }}</option>
                            {% for project in all_projects %}
                                {% ifnotequal info.belong_project project.project_name %}
                                    <option value="{{ project.project_name }}">{{ project.project_name }}</option>
                                {% endifnotequal %}
                                {% if info.belong_project != 'All' %}
                                    <option value="All">All</option>
                                {% endif %}

                            {% endfor %}
                        </select>
                    </li>
                        <button style="padding-top: 5px; margin-top: 9px"
                                class="am-btn am-radius am-btn-xs am-btn-success">搜索
                        </button>
                    </li>
                </form
            </form>
        </div>
        <form class="am-form am-g" id="project_list" name="project_list">
            <table width="100%" class="am-table am-table-bordered am-table-radius am-table-striped">
                <thead>
                    <tr class="am-success">
                        <th class="table-check"><input type="checkbox" id="select_all"/></th>
                        <th class="table-title">序号</th>
                        <th class="table-type">项目名称</th>
                        <th class="table-type">负责人</th>
                        <th class="table-title">发布应用</th>
                        <th class="table-title">测试人员</th>
                        <th class="table-title">模块/用例</th>
                        <th class="table-date am-hide-sm-only">创建时间</th>
                        <th width="163px" class="table-set">操作</th>
                    </tr>
                </thead>
                <tbody>
                    {% for project in projects %}
                    <tr>
                        <td><input type="checkbox" name="project_{{ project.id }}" value="{{ project.id }}"/></td>
                        <td>{{ forloop.counter }}</td>
                        <td><a href="#">{{ project.project_name }}</a></td>
                        <td>{{ project.responsible_name }}</td>
                        <td>{{ project.publish_app }}</td>
                        <td>{{ project.test_user }}</td>
                        <td>0</td>
                        <td class="am-hide-sm-only">{{ project.create_time }}</td>
                        <td>
                            <div class="am-btn-toolbar">
                                <div class="am-btn-group am-btn-group-xs">
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-secondary am-round"
                                            data-am-popover="{content: '运行', trigger: 'hover focus'}"
                                            onclick="#">
                                            <span class="am-icon-bug"></span>
                                    </button>
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-secondary am-round"
                                            data-am-popover="{content: '编辑', trigger: 'hover focus'}"
                                            onclick="edit('{{ project.id }}','{{ project.project_name }}', '{{ project.responsible_name }}'
                                                    , '{{ project.test_user }}','{{ project.dev_user }}', '{{ project.publish_app }}'
                                                    , '{{ project.simple_desc }}', '{{ project.other_desc }}')">
                                            <span class="am-icon-pencil-square-o"></span>
                                    </button>
                                    <button type="button"
                                            class="am-btn am-btn-default am-btn-xs am-text-danger am-round"
                                            data-am-popover="{content: '删除', trigger: 'hover focus'}"
                                            onclick="deleteProject('{{ project.id }}')">
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
                <button type="button" class="am-btn am-btn-default" onclick="location='{% url 'project_add'%}'"><span
                        class="am-icon-plus"></span> 新增
                </button>
            </div>

            <ul class="am-pagination am-fr">
                <span class="step-links">
                    {% if projects.has_previous %}
                    <a href="#" id='prepage' onclick="previous()">上一页</a>
                    {% endif %}
                </span>    
                <span class="current">
                    {{ projects.number }}/{{ projects.paginator.num_pages }} 页.
                </span>
                <span>
                    {% if projects.has_next %}
                        <a href="#" id='nextpage' onclick="next()"> 下一页</a>  
                     {% endif %}
                </span>
            </ul>
            <hr/>
        </form>
    </div>
    <script type="text/javascript">
        function edit(id, pro_name, responsible_name, test_user, dev_user, publish_app, simple_desc, other_desc) {
            $('#index').val(id);
            $('#project_name').val(pro_name);
            $('#responsible_name').val(responsible_name);
            $('#test_user').val(test_user);
            $('#dev_user').val(dev_user);
            $('#publish_app').val(publish_app);
            $('#simple_desc').val(simple_desc);
            $('#other_desc').val(other_desc);
            $('#my-edit').modal({
                relatedTarget: this,
                onConfirm: function () {
                    update_data_ajax('#edit_form', '{% url 'project_edit' %}')
                },
                onCancel: function () {
                }
            });
        }

        function deleteProject(id) {
            $('#delete-tip').modal({
                relatedTarget: this,
                onConfirm: function () {
                    del_data_ajax(id, '{% url 'project_delete' %}')
                },
                onCancel: function () {}
            });
        }
        

        
        

        $('#select_all').click(function () {
            var isChecked = $(this).prop("checked");
            $("input[name^='project']").prop("checked", isChecked);
        })

        {% if projects.has_next %}
        function next(){
           var params = $("#search").serialize() + "&page={{ projects.next_page_number }}";
           url = "{% url 'project_list' %}" + "?" + params
           $("#nextpage").attr('href',url); 
        }
        {% endif %}
        {% if projects.has_previous%}
        function previous(){
            var params = $("#search").serialize() + "&page={{ projects.previous_page_number }}";
           url = "{% url 'project_list' %}" + "?" + params
           $("#prepage").attr('href',url); 
        }
        {% endif %}
    </script>

{% endblock %}


```

访问 http://127.0.0.1:8000/httpapitest/project/list

### 修改base.html
修改base.html 使菜单 项目列表，和添加项目可用

```html
            <ul>
                <li><a href="{% url 'project_list' %}">项 目 列 表</a></li>
                <li><a href="{% url 'project_add' %}">新 增 项 目</a></li>
            </ul>
```

### 修改project_add试图
添加成功后跳转到项目列表页
```
    return HttpResponse(reverse('project_list'))
```
导入reverse 将`from django.urls import reverse`

###  project_list 模板编辑功能

需改commons.js添加以下代码

```js
function update_data_ajax(id, url) {
    var data = $(id).serializeJSON();
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

### 修改project_edit视图

```python
@csrf_exempt
def project_edit(request):
    if request.is_ajax():
        project = json.loads(request.body.decode('utf-8'))
        if project.get('project_name') == '':
            msg = '项目名称不能为空'
            return HttpResponse(msg)
        if project.get('responsible_name') == '':
            msg = '负责人不能为空'
            return HttpResponse(msg)
        if project.get('test_user') == '':
            msg = '测试人员不能为空'
            return HttpResponse(msg)
        if project.get('dev_user') == '':
            msg = '开发人员不能为空'
            return HttpResponse(msg)
        if project.get('publish_app') == '':
            msg = '发布应用不能为空'
            return HttpResponse(msg)
        else:
            p = Project.objects.get(project_name=project.get('project_name'))
            p.responsible_name = project.get('responsible_name')
            p.test_user = project.get('test_user')
            p.dev_user = project.get('dev_user')
            p.publish_app = project.get('publish_app')
            p.simple_desc = project.get('simple_desc')
            p.other_desc = project.get('other_desc')
            p.save()
            msg = 'ok'
        if msg == 'ok':
            return HttpResponse(reverse('project_list'))
        else:
            return HttpResponse(msg)        
```

点击编辑测试

### 修改project_list 添加删除功能

在commons.js 添加以下代码
```js
function del_data_ajax(id, url) {
    var data = {
        "id": id
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

修改project_delete视图
```python
@csrf_exempt
def project_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        project_id = data.get('id')
        project = Project.objects.get(id=project_id)
        project.delete()
        return HttpResponse(reverse('project_list'))
```

## debugtalk.py管理
每一个项目里都要有一个debugtalk.py文件用来定义一些函数，用来被配置文件引用


### 添加debugtalk url
```
path('debugtalk/edit/<int:id>', views.debugtalk_edit, name='debugtalk_edit'),
```



### 添加debugtalk 视图
debugtalk视图用来编辑debugtalk.py内容

```
@csrf_exempt
def debugtalk_edit(request, id):
    if request.method == "GET":
        d = DebugTalk.objects.get(pk=id)
        context_dict = {'debugtalk': d.debugtalk, 'id': d.id }
        return render(request, "debugtalk_edit.html",context_dict)

    if request.is_ajax():
        d = DebugTalk.objects.get(pk=id)
        content = json.loads(request.body.decode('utf-8'))
        d.debugtalk = content["debugtalk"]
        d.save()
        return HttpResponse("debugtalk edit success")
```


### 添加debugtalk_edit 模板
```
<!DOCTYPE html>
<html>
<head>
    <title>debugtalk.py</title>
    <meta charset="utf-8">
    {% load staticfiles %}
    <!--导入js库-->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.6/ace.js" type="text/javascript"
            charset="utf-8"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.6/ext-language_tools.js" type="text/javascript"
            charset="utf-8"></script>
    <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
    <script src="{% static 'assets/js/commons.js' %}"></script>
    <style>
        #login_click {
            margin-top: 32px;
            height: 40px;
        }

        #login_click a, #login_click button {

            text-decoration: none;
            background: #2f435e;
            color: #f2f2f2;

            padding: 10px 30px 10px 30px;
            font-size: 16px;
            font-family: 微软雅黑, 宋体, Arial, Helvetica, Verdana, sans-serif;
            font-weight: bold;
            border-radius: 3px;

            -webkit-transition: all linear 0.30s;
            -moz-transition: all linear 0.30s;
            transition: all linear 0.30s;

        }

        #login_click a:hover, #login_click button:hover {
            background: #385f9e;
        }
    </style>
</head>

<body>
<!--代码输入框（注意请务必设置高度，否则无法显示）-->
<pre id="code" class="ace_editor" style="margin-top: 0px; margin-bottom: 0px">
<textarea>
{{ debugtalk }}
</textarea>
</pre>

<div id="login_click" style="margin-top: 0px">
    <button id="push">点击提交</button>
    <a href="{% url 'project_list' %}">返回项目</a>
</div>


<script>
    //初始化对象
    editor = ace.edit("code");
    init_acs('python', 'monokai', editor);
    $(function () {
        var height = (window.screen.height - 180) + 'px';
        $('#code').css('min-height', height);
    });

    function post(url, params) {
        var temp = document.createElement("form");
        temp.action = url;
        temp.method = "post";
        temp.style.display = "none";
        for (var x in params) {
            var opt = document.createElement("input");
            opt.name = x;
            opt.value = params[x];
            temp.appendChild(opt);
        }
        document.body.appendChild(temp);
        temp.submit();
        return temp;
    }


    $('#push').click(function () {
        content = editor.session.getValue();
        $.ajax({
            type: 'POST',
            url: '{% url 'debugtalk_edit' id %}',
            data: JSON.stringify({debugtalk: content}),
            success: function(data){
            window.location='{% url 'project_list'%}'
             } ,
            contentType: 'application/json'
        });
        //post('{% url 'debugtalk_edit' id %}', {'debugtalk': content});
    });

</script>

</body>
</html>
```


在commons.js 文件中添加函数init_acs

```
function init_acs(language, theme, editor) {
    editor.setTheme("ace/theme/" + theme);
    editor.session.setMode("ace/mode/" + language);

    editor.setFontSize(17);

    editor.setReadOnly(false);

    editor.setOption("wrap", "free");

    ace.require("ace/ext/language_tools");
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        autoScrollEditorIntoView: true
    });


}
```

修改project_list.html模板

```html
<td>{{ forloop.counter }}</td>
<td><a href="{% url 'debugtalk_edit' project.debugtalk.id  %}">{{ project.project_name }}</a></td>
<td>{{ project.responsible_name }}</td>
```

测试，打开编辑页面修改代码然后提交
