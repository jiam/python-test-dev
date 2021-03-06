## 定时任务管理

1. 使用django-celery-beat 模块

安装
`pip install  django-celery-beat==1.5.0 -i https://pypi.douban.com/simple/`

在settings.py INSTALLED_APPS 中配置 django_celery_beat

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'httpapitest',
    'django_celery_beat',
]
```

需要执行下数据迁移，django_celery_beat 包含数据表

2. 添加视图

```python
@csrf_exempt
def task_add(request):
    """
    添加任务
    :param request:
    :return:
    """

    if request.is_ajax():
        kwargs = json.loads(request.body.decode('utf-8'))
        msg = task_logic(**kwargs)
        if msg == 'ok':
            return HttpResponse(reverse('task_list'))
        else:
            return HttpResponse(msg)
    elif request.method == 'GET':
        info = {
            'project': Project.objects.all().order_by('-create_time')
        }
        return render(request, 'task_add.html', info)

def task_list(request):
    if request.method == 'GET':
        name = request.GET.get('name','')
        info = {'name': name}
        if name:
            rs = PeriodicTask.objects.filter(name=name).order_by('-date_changed')
        else:
            rs = PeriodicTask.objects.all().order_by('-date_changed')
        paginator = Paginator(rs,5)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        context_dict = {'task': objects, 'info': info}
        return render(request,"task_list.html",context_dict)


@csrf_exempt
def task_delete(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        task_id = data.get('id')
        task = PeriodicTask.objects.get(id=task_id)
        task.delete()
        return HttpResponse(reverse('task_list'))

@csrf_exempt
def task_set(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        task_id = data.get('id')
        mode = data.get('mode')
        task = PeriodicTask.objects.get(id=task_id)
        task.enabled = mode
        task.save()
        return HttpResponse(reverse('task_list'))
```

veiws.py 新增导入

```python
from django_celery_beat.models import PeriodicTask
from httpapitest.utils import task_logic
```

2. utils.py 添加task_logic函数
```python
def task_logic(**kwargs):
    """
    定时任务逻辑处理
    :param kwargs: dict: 定时任务数据
    :return:
    """
    
    if kwargs.get('name') is '':
        return '任务名称不可为空'
    elif kwargs.get('project') == '请选择':
        return '请选择一个项目'
    elif kwargs.get('crontab_time') is '':
        return '定时配置不可为空'
    elif kwargs.get('module') == '请选择' :
        return '请选择模块'
    kwargs.pop('project')        
    try:
        crontab_time = kwargs.pop('crontab_time').split(' ')
        if len(crontab_time) > 5:
            return '定时配置参数格式不正确'
        crontab = {
            'day_of_week': crontab_time[-1],
            'month_of_year': crontab_time[3],  # 月份
            'day_of_month': crontab_time[2],  # 日期
            'hour': crontab_time[1],  # 小时
            'minute': crontab_time[0],  # 分钟
        }
    except Exception:
        return '定时配置参数格式不正确'
    if PeriodicTask.objects.filter(name__exact=kwargs.get('name')).count() > 0:
        return '任务名称重复，请重新命名'
    desc = " ".join(str(i) for i in crontab_time)
    name = kwargs.get('name')

    return create_task(name, 'httpapitest.tasks.module_hrun', kwargs, crontab, desc)
```
在utils.py 导入
```
from httpapitest.tasks_opt import create_task
from django_celery_beat.models import PeriodicTask
```

3. 在httpapitest目录下添加tasks_opt.py
```
import json

from django_celery_beat import models as celery_models


def create_task(name, task, task_args, crontab_time, desc):
    '''
    新增定时任务
    :param name: 定时任务名称
    :param task: 对应tasks里已有的task
    :param task_args: list 参数
    :param crontab_time: 时间配置
    :param desc: 定时任务描述
    :return: ok
    '''
    # task任务， created是否定时创建
    task, created = celery_models.PeriodicTask.objects.get_or_create(name=name, task=task)
    # 获取 crontab
    crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()
    if crontab is None:
        # 如果没有就创建，有的话就继续复用之前的crontab
        crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
    task.crontab = crontab  # 设置crontab
    task.enabled = True  # 开启task
    print(task_args)
    task.kwargs = json.dumps(task_args)  # 传入task参数
    task.description = desc
    task.save()
    return 'ok'


def change_task_status(name, mode):
    '''
    任务状态切换：open or close
    :param name: 任务名称
    :param mode: 模式
    :return: ok or error
    '''
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        task.enabled = mode
        task.save()
        return 'ok'
    except celery_models.PeriodicTask.DoesNotExist:
        return 'error'


def delete_task(name):
    '''
    根据任务名称删除任务
    :param name: task name
    :return: ok or error
    '''
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        task.enabled = False  # 设置关闭
        task.delete()
        return 'ok'
    except celery_models.PeriodicTask.DoesNotExist:
        return 'error'
```
commons.js添加函数
```js
/*添加计划任务*/
function task_add(url) {
    // 使用jquery获取表单数据
    var data = $('#task_add').serializeJSON(); 

    // 对表单数据做校验
    if (data.project === '请选择' ) {
        myAlert('请选择项目')
        return
    }
    if (data.name === '') {
        myAlert('名字不能为空')
        return
    }

    if (data.module === '') {
        myAlert('请选择模块')
        return
    }

    if (data.crontab_time === '') {
        myAlert('定时配置不可为空')
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


4. 添加模板

[task_add.html](./Chapter-13-code/hat/templates/task_add.html)
[task_list.html](./Chapter-13-code/hat/templates/task_list.html)

5. 添加url
```
    path('task/add', views.task_add, name='task_add'),
    path('task/list',views.task_list, name='task_list'),
    path('task/delete', views.task_delete, name="task_delete"),
    path('task/set', views.task_set, name="task_set"),
```
6. 启动celery定时任务
`celery -A  hat  beat  --loglevel=info`
启动worker
`celery -A  hat  worker --loglevel=info  -P gevent`

测试添加任务

## 用例个数统计功能

1. 在templatetags 目录下的caustom_tags.py中添加
```python
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
    sum = test_countmodule_sum
    return sum
```
导入`from httpapitest.models import Module,TestCase`
2. 将project_list.html 中的0 修改为 `{{ project.project_name | project_sum }}` 并在文件头部添加`{% load custom_tags %}`
3. 将module_list.html中的0修改为`{{ module.id |  }}` 并在文件头部添加`{% load custom_tags %}`

## dashboard

1. 修改index的模板
index.html修改为以下链接中的内容

[index.html](./Chapter-13/code/hat/templates/index.html)


2. 修改index视图
```python
def index(request):
    project_length = Project.objects.count()
    module_length = Module.objects.count()
    test_length = TestCase.objects.count()
    

    total = get_total_values()
    manage_info = {
        'project_length': project_length,
        'module_length': module_length,
        'test_length': test_length,
        'total': total
    }

    
    return render(request, 'index.html', manage_info)
```
导入'from httpapitest.utils import get_total_values'

3. utils.py添加get_total_values 函数
```python
def get_total_values():
    total = {
        'pass': [],
        'fail': [],
        'percent': []
    }
    today = datetime.date.today()
    for i in range(-11, 1):
        begin = today + datetime.timedelta(days=i)
        end = begin + datetime.timedelta(days=1)

        total_run = TestReports.objects.filter(create_time__range=(begin, end)).aggregate(testRun=Sum('testsRun'))[
            'testRun']
        total_success = TestReports.objects.filter(create_time__range=(begin, end)).aggregate(success=Sum('successes'))[
            'success']

        if not total_run:
            total_run = 0
        if not total_success:
            total_success = 0

        total_percent = round(total_success / total_run * 100, 2) if total_run != 0 else 0.00
        total['pass'].append(total_success)
        total['fail'].append(total_run - total_success)
        total['percent'].append(total_percent)

    return total
```
导入`from django.db.models import Sum`

## 登录，注册，退出功能
1. 在添加models.py 中添加类
```python
class UserInfo(BaseTable):
    class Meta:
        verbose_name = '用户信息'
        db_table = 'UserInfo'

    username = models.CharField('用户名', max_length=20, unique=True, null=False)
    password = models.CharField('密码', max_length=20, null=False)
    email = models.EmailField('邮箱', null=False, unique=True)
    status = models.IntegerField('有效/无效', default=1)
    objects = UserInfoManager()
```
在models.py中导入
`from httpapitest.managers import UserInfoManager`
2. 在managers.py 中添加类
```
class UserInfoManager(models.Manager):
    def insert_user(self, username, password, email, object):
        self.create(username=username, password=password, email=email, user_type=object)

    def query_user(self, username, password):
        return self.filter(username__exact=username, password__exact=password).count()
```

3. 添加视图函数
```python
def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')

        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            logging.info('{username} 登录成功'.format(username=username))
            request.session["login_status"] = True
            request.session["now_account"] = username
            return redirect('index')
        else:
            logging.info('{username} 登录失败, 请检查用户名或者密码'.format(username=username))
            return render(request, 'login.html', {'msg': '账号或密码不正确'})
    elif request.method == 'GET':
        return render(request, 'login.html')

@csrf_exempt
def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.is_ajax():
        user_info = json.loads(request.body.decode('utf-8'))
        try:
            username = user_info.get('account')
            password = user_info.get('password')
            email = user_info.get('email')
    
            if UserInfo.objects.filter(username__exact=username).filter(status=1).count() > 0:
                logging.debug('{username} 已被其他用户注册'.format(username=username))
                msg = '该用户名已被注册，请更换用户名'
            if UserInfo.objects.filter(email__exact=email).filter(status=1).count() > 0:
                logging.debug('{email} 昵称已被其他用户注册'.format(email=email))
                msg = '邮箱已被其他用户注册，请更换邮箱'
            else:
                UserInfo.objects.create(username=username, password=password, email=email)
                logging.info('新增用户：{user_info}'.format(user_info=user_info))
                msg =  'ok'
        except Exception as e:
            logging.error('信息输入有误：{user_info}'.format(user_info=user_info))
            msg =  e
        if msg == 'ok':
            return HttpResponse('恭喜您，账号已成功注册')
        else:
            return HttpResponse(msg)
    elif request.method == 'GET':
        return render(request, "register.html")


def logout(request):
    """
    注销登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        logging.info('{username}退出'.format(username=request.session['now_account']))
        del request.session['now_account']
        del request.session['login_status']
        return redirect(login)

```
views.py导入
```
from httpapitest.models import UserInfo
from django.shortcuts import redirect
```


4. 添加模板

[login.html](./Chapter-13/code/hat/templates/login.html)
[register.html](./Chapter-13/code/hat/templates/register.html)

hat.urls.py 添加
```python
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
```

修改base.html
注销关联的url
 `href='{% url 'logout' %}'>注 销</a>`

## 权限限制
1. 在views.py 导入语句的下面添加 login_check 装饰器

```
def login_check(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('login_status'):
            return redirect(login)
        return func(request, *args, **kwargs)

    return wrapper
```
 5. 在所有视图函数上添加 `@login_check` login和register函数除外,因为这两个不需要登录



 ## 测试环境
被测服务一个flask应用[api_server.py](./Chapter-13/code/demo/api_server.py)

`pip install flask`

该应用作为被测服务，主要有两类接口：

* 权限校验，获取 token
* 支持 CRUD 操作的 RESTful APIs，所有接口的请求头域中都必须包含有效的 token

下载文件api_server.py,执行以下命令运行
`python api_server.py `
api_server.py包括一下功能
1. index 返回hello world
    ```
    path: /
    method: get
    params: 无
    ```
    例子：
    `curl 127.0.0.1:5000`
2. get_token 获取认证token
    ```
    path: /api/get-token
    method: post
    header：device_sn，os_platform，app_version
    数据格式： json
    内容： {"sign":"xxxx"}
    ```
    例子：
    `curl -H "device_sn:123456" -H "os_platform:ios" -H "app_version:v1" -H "Content-Type:application/json" -d '{"sign":"4d11fd0929db6d0df9dfdec5329a2f9c5b53ba1c"}' http://127.0.0.1:5000/api/get-token`
3. get_users 获取用户列表
   ```
   path: /api/users
   method: get
   header: device_sn,token
   ```
   例子：
   `curl -H "device_sn:123456" -H "token:T9OI65aASKcHqeaH"   http://127.0.0.1:5000/api/users`
4. create_user 创建用户
    ```
    path：/api/users/uid
    method：post
    header: device_sn,token
    数据格式： json
    数据内容：{"user":"test"}
    ```
    例子
    `
     curl -XPOSt -H "device_sn:123456" -H "token:cnSQdjGu1D7XzK8l" -H "Content-Type:application/json"   http://127.0.0.1:5000/api/users/1004 -d '{"name":"test","password":"test"}'
      `
5. get_user 获取用户信息
    ```
    path：/api/users/uid
    method：post
    header: device_sn,token
    ```
    例子
    ·curl -H "device_sn:123456" -H "token:cnSQdjGu1D7XzK8l"   http://127.0.0.1:5000/api/users/1004
{"success": true, "data": {"name": "test", "password": "test"}}·

6. update_user 更新用户信息
    ```
    path：/api/users/uid
    method：put
    header: device_sn,token
    数据格式： json
    数据内容：{"user":"test"}
    ```

   例子
   `curl -XPUT -H "device_sn:123456" -H "token:cnSQdjGu1D7XzK8l" -H "Content-Type:application/json"   http://127.0.0.1:5000/api/users/1004 -d '{"name":"test","password":"test2"}'
`
7. delete_user 删除用户信息
    ```
    path：/api/users/uid
    method：delete
    header: device_sn,token

    ```
例子
`curl -XDELETE -H "device_sn:123456" -H "token:cnSQdjGu1D7XzK8l"   http://127.0.0.1:5000/api/users/1004 
{"success": true, "data": {"name": "test", "password": "test2"}}`

### 简单例子
1. 新建项目
![img](./Chapter-13/code/pics/新建项目.png)

2. 新增模块
![img](./Chapter-13/code/pics/新建模块.png)

3. 新增测试用例
![img](./Chapter-13/code/pics/新建用例-1.jpg)
![img](./Chapter-13/code/pics/新建用例-2.png)
![img](./Chapter-13/code/pics/新建用例-3.png)

4. 运行用例

![img](./Chapter-13/code/pics/运行结果.png)

### 高级用例
一、get_token 用例
1. 编写debugtalk
```
#debugtalk.py

import hashlib
import hmac
import random
import string

SECRET_KEY = "DebugTalk"

def gen_random_string(str_len):
    random_char_list = []
    for _ in range(str_len):
        random_char = random.choice(string.ascii_letters + string.digits)
        random_char_list.append(random_char)

    random_string = ''.join(random_char_list)
    return random_string

def get_sign(*args):
    content = ''.join(args).encode('ascii')
    sign_key = SECRET_KEY.encode('ascii')
    sign = hmac.new(sign_key, content, hashlib.sha1).hexdigest()
    return sign
```

2. 定义变量
![img](./Chapter-13/code/pics/get_token-变量.jpg)

|变量名     | 变量值                   |
|----------|--------------------------|
| device_sn  | ${gen_random_string(15)}|
| os_platform| win10                  |
| app_version| 2.8.6                   |

注： ${gen_random_string(15)} 是debugtalk中定义的函数gen_random_string(str_len)       |

3. 定义请求方法和数据
![img](./Chapter-13/code/pics/get_token-json.jpg)

url http://127.0.0.1:5000/api/get-token

方法 post
json
```
{
    "sign": "${get_sign($device_sn, $os_platform, $app_version)}"
}
```
get_sign 为debugtalk中定义的函数$和大括号不能丢
参数为我们刚才定义的变更
4. 定义header
![img](./Chapter-13/code/pics/get_token-header.jpg)

|key     | value                |
|----------|--------------------|
| device_sn  | $device_sn       |
| os_platform| $os_platform     |
| app_version| $app_version     |

二、create_user 用例
1. 定义数据与header
![img](./Chapter-13/code/pics/create_user-header.jpg)
url http://127.0.0.1:5000/api/users/1000

json
```
{
    "name": "test",
    "password": "test"
}

```

header
|key     | value                |
|----------|--------------------|
| device_sn| 12345     |
| token    | $token    |

2. 断言

![img](./Chapter-13/code/pics/create_user-assert.jpg)
status_code 201

3. 添加依赖

![img](./Chapter-13/code/pics/create_user-dep.jpg)

创建用户接口需要一个token，该token可以通过get_token 接口获取

修个get_token 用例添加一个提取
![img](./Chapter-13/code/pics/get_token-extract.jpg)
token    content.token

并将get_token用例中的变量 device_sn改为123456

练习修改用户接口

## httprunner

平台底层使用的是httprunnnr进行接口测试，运行测试时会在项目的根目录下有个sutie目录,每次运行都会在suite目录下产生一个时间格式的目录
```
hat/suite# ls
'2021-02-28 14-35-12-412'  '2021-02-28 14-49-42-857'  '2021-03-06 14-07-41-004'  '2021-03-06 14-18-34-437'  '2021-03-06 14-45-12-737'  '2021-03-06 15-00-50-896'   reports
'2021-02-28 14-36-28-064'  '2021-03-06 13-56-44-754'  '2021-03-06 14-14-44-314'  '2021-03-06 14-26-27-323'  '2021-03-06 14-46-54-131'  '2021-03-06 15-01-39-756'
'2021-02-28 14-36-58-074'  '2021-03-06 13-58-57-868'  '2021-03-06 14-17-06-369'  '2021-03-06 14-44-36-376'  '2021-03-06 14-56-08-401'  '2021-03-06 15-01-58-616'
```

目录结构如下
```
tree '2021-03-06 15-01-58-616'
2021-03-06 15-01-58-616
├── apiserver测试
│   └── 测试首页
│       └── create-user.yml
└── debugtalk.py

2 directories, 2 files

```
里面包含我们项目中的debugtalk.py文件和测试用例文件xxx.yml

yml格式如下
```
-   config:
        base_url: ''
        name: create-user
-   test:
        extract:
        -   token: content.token
        name: get-token
        request:
            headers:
                app_version: $app_version
                device_sn: $device_sn
                os_platform: $os_platform
            json:
                sign: ${get_sign($device_sn, $os_platform, $app_version)}
            method: POST
            url: http://127.0.0.1:5000/api/get-token
        validate:
        -   check: status_code
            comparator: equals
            expect: 200
        variables:
        -   device_sn: '123456'
        -   os_platform: ios
        -   app_version: v1
-   test:
        name: create-user
        request:
            headers:
                device_sn: '123456'
                token: $token
            json:
                name: test
                password: test
            method: POST
            url: http://127.0.0.1:5000/api/users/1004
        validate:
        -   check: status_code
            comparator: equals
            expect: 201

```

我们平台的创建用例就是生成这个yml的文件，运行用例就使用httprunner跑用例

runner.py 中的 run_by_single函数作用就是生成上面的测试目录结构，包括debugtalk.py和yml文件

执行测试用例代码，views.py中的test_run和test_batch_run
```
run_test_by_type(id, base_url, testcase_dir_path, type) #生成测试目录
runner.run(testcase_dir_path) #使用httprunner的run方法，启动测试用例
```
我们也可以直接使用httprunner提供的命令hrun来运行测试用例
```
root@myhub:/opt/hat/suite/2021-03-06 15-01-58-616# hrun  ./
INFO     Start to run testcase: create-user
get-token
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time(ms): 8.39 ms, response_length: 46 bytes

.
create-user
INFO     POST http://127.0.0.1:5000/api/users/1004
INFO     status_code: 201, response_time(ms): 9.33 ms, response_length: 54 bytes

.

----------------------------------------------------------------------
Ran 2 tests in 0.020s

OK
INFO     Start to render Html report ...
INFO     Generated Html report: /opt/hat/suite/2021-03-06 15-01-58-616/reports/1615016134.html

```

yml配置文件
extract 和 validate 常用字段 
```
response content could be json or html text.

        Args:
            field (str): string joined by delimiter.
            e.g.
                "status_code"
                "headers"
                "cookies"
                "content"
                "headers.content-type"
                "content.person.name.first_name"
```








