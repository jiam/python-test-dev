# django
[toc]
##  Django介绍
Django是一个高级Python Web框架，鼓励快速开发和实用的设计。
由经验丰富的开发人员开发，它可以处理Web开发的大部分问题，
因此可以专注于编写应用程序，而无需重新发明轮子。

Django 特点
1.  快速: Django旨在帮助开发人员尽可能快地完成应用程序
2.  安全: Django严肃对待安全并帮助开发人员避免许多常见的安全错误
3.  可伸缩:  Django快速灵活扩展的能力
4.  丰富的组件: Django 内置各种web开发常用功能组件

Djaong框架
![django框架](./Chapter-07/pics/django.jfif)

## Django安装

使用pip
```
pip install django==2.2.2 -i https://pypi.douban.com/simple
```

验证django
```python
>>> import django
>>> django.get_version()
'2.2.2'
```

## 请求和相应
创建第一个django项目，开发一个投票网站
### 创建项目

进入你想放置代码的目录，然后运行以下命令：

`django-admin startproject mysite`
这行代码将会在当前目录下创建一个 mysite 目录。

mystie目录结构
```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```



+ 最外层的 mysite/ 根目录， 你可以将它重命名为任何你喜欢的名字。
+ manage.py: 管理 Django 项目的命令行工具。。
+ 里面一层的 mysite/ 目录包含项目相关配置，它是一个纯 Python 包。
+ mysite/__init__.py：一个空文件，告诉 Python 这个目录应该被认为是一个 Python 包。
+ mysite/settings.py：Django 项目的配置文件。如果你想知道这个文件是如何工作的，请查看 Django 配置 了解细节。
+ mysite/urls.py：Django 项目的 URL 声明，是网站的“目录”
+ mysite/wsgi.py：作为你的项目的运行在 WSGI 兼容的Web服务器上的入口，比如gunicorn

### 启动开发服务器

进入项目根目录，既manage.py文件所在目录,运行以下命令
`python manage.py runserver`

输出如下：
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
December 21, 2020 - 21:21:04
Django version 2.2.7, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

刚刚启动的是 Django 自带的用于开发的服务器，它是一个用纯 Python 写的轻量级的 Web 服务器。这个服务器内置在 Django 中是为了能快速的开发出想要的东西，不要用于生产环境。

浏览器访问 http://127.0.0.1:8000/

>默认情况下，runserver 命令会将服务器设置为监听本机内部 IP 的 8000 端口。
>
>指定端口启动
>
>`python manage.py runserver 8080`
>
>指定监听的IP
>
>`python manage.py runserver 0.0.0.0:8000`

监听机器上的所有ip


### 创建应用

在 Django 中，每一个应用都是一个 Python 包，并且遵循着相同的约定。Django可以帮你生成应用的基础目录结构，这样你就能专心写代码，而不是创建目录了。

>项目和应用有啥区别
>
>应用是一个专门做某件事的网络应用程序——比如博客系统，或者公共记录的数据库，或者简单的投票程序。项目则是一个网站使用的配置和应用的集合。项目可以包含很多个应用。应用可以被很多个项目使用。

确定你现在处于 manage.py 所在的目录下，然后运行这行命令来创建一个应用：
 
`python manage.py startapp polls`

这将会创建一个 polls 目录，它的目录结构大致如下：
```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```



### 编写第一个视图

polls/views.py
```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

这是 Django 中最简单的视图。如果想看见效果，我们需要将一个 URL 映射到它——这就是我们需要 URLconf 的原因了。

为了创建 URLconf，请在 polls 目录里新建一个 urls.py 文件。你的应用目录现在看起来应该是这样

```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py
```
在 polls/urls.py 中，输入如下代码：
```python

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

下一步是要在根 URLconf 文件中指定我们创建的 polls.urls 模块。在 mysite/urls.py 文件的 urlpatterns 列表里插入一个 include()， 如下：

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

函数 include() 允许引用其它 URLconfs。每当 Django 遇到 include() 时，它会截断与此项匹配的 URL 的部分，并将剩余的字符串发送到 URLconf 以供进一步处理。

浏览器访问http://127.0.0.1:8000/polls/

>函数 path() 具有四个参数，两个必须参数：route 和 view，两个可选参数：kwargs 和 name。
>
>**route参数** 是一个匹配 URL 的字符串。它会从 urlpatterns 的第一项开始，按顺序依次匹配列表中的项，直到找到匹配的项。
>
>这些准则不会匹配 GET 和 POST 参数或域名。例如，URLconf 在处理请求 https://www.example.com/myapp/ 时，它会尝试匹配 myapp/ 。处理请求 https://www.example.com/myapp/?page=3 时，也只会尝试匹配 myapp/。
>
>**view参数** 是一个视图函数，当 Django 找到了一个匹配，就会调用这个特定的视图函数，并传入一个 HttpRequest 对象作为第一个参数
>
>**kwargs参数** 将一个字典传给视图函数
>
>**name参数**，为你的 URL 取名能使你在 Django 的任意地方唯一地引用它，尤其是在模板中。这个有用的特性允许你只改urls.py就能全局地修改某个 URL 模式。

## 模型和admin站点

### 数据库配置
打开 mysite/settings.py 

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

默认数据库为sqlite，这是个文件数据库，文件名为db.sqlite3

>**ENGINE** 为数据库类型，可选值为： 'django.db.backends.sqlite3'，'django.db.backends.postgresql'，'django.db.backends.mysql'，或 'django.db.backends.oracle'。
>**name** 数据库的名称。如果使用的是 SQLite，数据库将是一个文件，在这种情况下， NAME 是此文件的绝对路径，包括文件名。默认值 os.path.join(BASE_DIR, 'db.sqlite3') 将会把数据库文件储存在项目的根目录。

如果不使用 SQLite，则必须添加一些额外设置，比如 USER 、 PASSWORD 、 HOST 等等。mysql例子
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
设置语言为中文

`LANGUAGE_CODE = 'zh-hans'`

INSTALLED_APPS设置项,这里包括了会在项目中启用的Django 应用。默认包括了以下 Django 的自带应用
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
+ django.contrib.admin -- 管理员站点， 你很快就会使用它。
+ django.contrib.auth -- 认证授权系统。
+ django.contrib.contenttypes -- 内容类型框架。
+ django.contrib.sessions -- 会话框架。
+ django.contrib.messages -- 消息框架。
+ django.contrib.staticfiles -- 管理静态文件的框架。

在使用这些应用之前需要在数据库中创建一些表。确认在manager.py 文件所在目录，执行以下命令

`python manage.py migrate`

输出如下：
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK
```
 migrate 命令检查 INSTALLED_APPS 设置，为其中的每个应用创建需要的数据表

执行命令,访问sqlite数据库
`sqlite3.exe db.sqlite3`

查看创建的表
```
sqlite> .table
auth_group                  auth_user_user_permissions
auth_group_permissions      django_admin_log
auth_permission             django_content_type       
auth_user                   django_migrations
auth_user_groups            django_session
```
### 创建模型

在这个投票网站中，需要创建两个模型：问题 Question 和选项 Choice。Question 模型包括问题描述和发布时间。Choice 模型有两个字段，选项描述和当前得票数。

编辑 polls/models.py 文件
```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
每个类被表示为 django.db.models.Model 类的子类。每个类有一些类变量，它们都表示模型里的一个数据库字段。每个类都会队以应一个表

每个字段都是 Field 类的实例 - 比如，字符字段被表示为 CharField ，日期时间字段被表示为 DateTimeField 。这将告诉 Django 每个字段要处理的数据类型。

每个 Field 类实例变量的名字（例如 question_text 或 pub_date ）也是字段名。

ForeignKey 定义了一个关系。这将告诉 Django，每个 Choice 对象都关联到一个 Question 对象。Django 支持所有常用的数据库关系：多对一、多对多和一对一。

### 使用模型

首先，需要在配置文件mysite/settings.py 中启用应用

```python
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
现在 项目会包含 polls 应用。接着运行下面的命令

`python manage.py makemigrations polls`

输出如下：
```
Migrations for 'polls':
  polls\migrations\0001_initial.py
    - Create model Question       
    - Create model Choice
```

通过运行 makemigrations 命令，Django 会检测你对模型文件的修改，并且把修改的部分储存为一次 migration。migration 被存放在polls/migrations目录下polls/migrations/0001_initial.py

Django 有一个自动执行数据库migration，同步到数据库的命令 - migrate


我们先来看看migrate 会执行那些语句，执行

`python manage.py sqlmigrate polls 0001`

输出如下：
```sql
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" integer NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;
```
执行migrate

`python manage.py migrate`

输出如下：
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Applying polls.0001_initial... OK
```

migrate 命令选中所有还没有执行过的迁移（Django 通过在数据库中创建一个特殊的表 django_migrations 来跟踪执行过哪些migtation）并应用在数据库上 - 也就是将你对模型的更改同步到数据库结构上

migration是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表 - 它专注于使数据库平滑升级而不会丢失数据。

现在，需要记住，改变模型需要这三步：
+ 编辑 models.py 文件，改变模型。
+ 运行 python manage.py makemigrations 为模型的改变生成migration文件。
+ 运行 python manage.py migrate 来同步到数据库。

### django交互shell

通过以下命令打开django交互命令

`python manage.py shell`

尝试执行下语句
```python
>>> from polls.models import Choice, Question #导入模型类
>>> Question.objects.all()  #查询所有 Question
<QuerySet []>
>>> from django.utils import timezone # 导入时区
>>> q = Question(question_text="What's new?", pub_date=timezone.now()) #创建一个Question
>>> q.save() #存入数据库
>>> q.id  # 查询id
1
>>> q.question_text #查询 question_text 字段
"What's new?"
>>> q.pub_date  
datetime.datetime(2020, 12, 22, 13, 15, 23, 3355, tzinfo=<UTC>)
>>> q.question_text = "What's up?"
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```

这里注意`<Question: Question object (1)>`只是个对象没有其它有用信息

让我们通过编辑 Question 模型的代码（位于 polls/models.py 中）来修复这个问题。给 Question 和 Choice 增加 __str__() 方法。

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
```
>注意：添加方法不需要进行migration

```python
>>> from polls.models import Choice, Question                          
>>> Question.objects.all()                     
<QuerySet [<Question: What's new?>]>
```

我们再给Question添加一个方法was_published_recently，判断是否最近的投票

```python
from django.db import models
from django.utils import timezone
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
```

再次练习

```python
>>> from polls.models import Choice, Question
>>> Question.objects.all()
<QuerySet [<Question: What's new?>]>
>>> Question.objects.filter(id=1)  # 查询id为1的记录
<QuerySet [<Question: What's new?>]>
>>> Question.objects.filter(question_text__startswith='What') #查询question_text字段的值以What开始的记录
<QuerySet [<Question: What's new?>]>
>>> from django.utils import timezone
>>> current_year = timezone.now().year  #日期年
>>> Question.objects.get(pub_date__year=current_year) #查询创建日期年等于current_year
<Question: What's new?>
>>> Question.objects.get(id=2)  # 查询id为2的记录，不存在返回异常
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "D:\python\python-dev\venv\lib\site-packages\django\db\models\manager.py", line 82, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
    self.model._meta.object_name
polls.models.Question.DoesNotExist: Question matching query does not exist.
>>> Question.objects.get(pk=1)
<Question: What's new?>
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()   #调用was_published_recently方法
True
>>> q = Question.objects.get(pk=1)
>>> q.choice_set.all()   # 查询问题的所有选项
<QuerySet []>
>>> q.choice_set.create(choice_text='Not much', votes=0) # 创建问题选项
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
>>> c.question  # 查询选项关联的问题
<Question: What's new?>
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count() # 返回选项的数量
3
>
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()  # 删除选项
(1, {'polls.Choice': 1})
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>]>
```

### django 管理界面
创建能登录管理界面的用户

```
python manage.py createsuperuser
Username (leave blank to use 'wang_'): admin
Email address: 260137162@qq.com
Password: 
Password (again): 
Superuser created successfully.
```

启动开发服务器

`python manage.py runserver`

打开浏览器输入http://127.0.0.1:8000/admin/

向管理后台中加入polls应用，我们得告诉管理页面，Question 对象需要被管理。打开 polls/admin.py 文件

```python
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

再打开浏览器可以看到到polls应用和Question

此时可以看到应用名和字段名都为英文
编辑polls/models.py
```python
class Question(models.Model):
    question_text = models.CharField('问题',max_length=200)
    pub_date = models.DateTimeField('发布时间')
    class Meta:
        verbose_name = '问题'
        verbose_name_plural = '问题'

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```

编辑polls/apps.py
```python
from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'
    verbose_name = '投票'

```

刷新浏览器查看，应用与字段名已变成自定义的名字

练习：
向管理界面添加Choice模型

## 视图和模板

### 视图

在我们的投票应用中，我们需要下列几个视图：
+ 投票索引页——展示最近的几个投票问题。
+ 跳票详情页——展示某个投票的问题和不带结果的选项列表。
+ 投票结果页——展示某个投票的结果。
+ 投票处理器——用于响应用户为某个问题的特定选项投票的操作。

在 Django 中，网页和其他内容都是从视图派生而来。每一个视图表现为一个简单的 Python 函数（或者说方法，如果是在基于类的视图里的话）。Django 将会根据用户请求的 URL 来选择使用哪个视图（更准确的说，是根据 URL 中域名之后的部分）。


### 创建视图

编辑polls/views.py,添加视图

```python
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```
把这些新视图添加进 polls.urls


```python
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

然后看看你的浏览器，如果你转到 "/polls/5/" ，Django 将会运行 detail() 方法并且展示你在 URL 里提供的问题 ID。再试试 "/polls/5/results/" 和 "/polls/5/vote/" ——你将会看到暂时用于占位的结果和投票页

当某人请求网站的某一页面时——比如说， "/polls/5/" ，Django 将会载入 mysite.urls 模块，因为这在配置项 ROOT_URLCONF 中设置了。然后 Django 寻找名为 urlpatterns 变量并且按序匹配正则表达式。在找到匹配项 'polls/'，它切掉了匹配的文本（"polls/"），将剩余文本——"5/"，发送至 'polls.urls' URLconf 做进一步处理。在这里剩余文本匹配了 '<int:question_id>/'，使得我们 Django 以如下形式调用 detail():

`detail(request=<HttpRequest object>, question_id=5)

question_id=5 由 `<int:question_id>`匹配生成。使用`<>`“捕获”这部分 URL，且以关键字参数的形式发送给视图函数。上述字符串的 question_id 部分定义了将被用于区分匹配模式的变量名，而 int: 则是一个转换器决定了应该以什么变量类型匹配这部分的 URL 

### 编写一个有意义的视图

每个视图必须要做的只有两件事：返回一个包含被请求页面内容的 HttpResponse 对象，或者抛出一个异常，比如 Http404 

你的视图可以从数据库里读取记录，可以使用一个模板引擎（比如 Django 自带的，或者其他第三方的），可以生成一个 PDF 文件，可以输出一个 XML，创建一个 ZIP 文件，你可以做任何你想做的事，使用任何你想用的 Python 库。

Django 只要求返回的是一个 HttpResponse ，或者抛出一个异常

尝试在视图中使用数据库数据

修改 polls/views.py
```python
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
```
按时间排序返回前5个投票问题

这里有个问题：页面的设计写死在视图函数的代码里的。如果你想改变页面的样子，你需要编辑 Python 代码。所以让我们使用 Django 的模板系统，只要创建一个视图，就可以将页面的设计从代码中分离出来。

首先，在你的 polls 目录里创建一个 templates 目录。Django 将会在这个目录里查找模板文件

mysite/settings.py中的 TEMPLATES 配置项描述了 Django 如何载入和渲染模板。默认的设置文件设置了 DjangoTemplates 后端，并将 APP_DIRS 设置成了 True。这一选项将会让 DjangoTemplates 在每个 INSTALLED_APPS 文件夹中寻找 "templates" 子目录。

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

在你刚刚创建的 templates 目录里，再创建一个目录 polls，然后在其中新建一个文件 index.html 。换句话说，你的模板文件的路径应该是 polls/templates/polls/index.html 。因为 Django 会寻找到对应的 app_directories ，所以你只需要使用 polls/index.html 就可以引用到这一模板了。

创建polls/templates/polls/index.html
```html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

然后，让我们更新一下 polls/views.py 里的 index 视图来使用模板：
```python
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

上述代码的作用是，载入 polls/index.html 模板文件，并且向它传递一个上下文(context)。这个上下文是一个字典，它将模板内的变量映射为 Python 对象。

用你的浏览器访问 "/polls/" ，你将会看见一个无序列表，列出了投票问题，链接指向这个投票的详情页。

### render 函数

「载入模板，填充上下文，再返回由它生成的 HttpResponse 对象」是一个非常常用的操作流程。于是 Django 提供了一个快捷函数，我们用它来重写 index() 视图：

```python
from django.http import HttpResponse
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

render（）函数将请求对象(request)作为其第一个参数，将模板名称作为其第二个参数，并将字典作为其可选的第三个参数。它返回使用给定上下文呈现的给定模板的HttpResponse对象。


### 抛出404

现在，我们来处理投票详情视图——它会显示指定投票的问题。下面是这个视图的代码：

```python
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```
如果指定问题 ID 所对应的问题不存在，这个视图就会抛出一个 Http404 异常

为了能是视图工作，我们创建一个简单的模板polls/templates/polls/detail.html
```
{{ question }}
```

### get_object_or_404函数

尝试用 get() 函数获取一个对象，如果不存在就抛出 Http404 错误也是一个普遍的流程。Django 也提供了一个快捷函数，下面是修改后的详情 detail() 视图代码：
```python
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```

get_object_or_404（）函数将Django模型作为其第一个参数，并将任意数量的关键字参数传递给模型管理器的get（）函数。如果对象不存在，它将引发Http404。

### 修改投票详情模板
编辑polls/templates/polls/detail.html
```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

模板系统统一使用点符号来访问变量的属性。在示例 {{ question.question_text }} 中，访问question的question_text属性

在 {% for %} 循环中发生的函数调用：question.choice_set.all 被解释为 Python 代码 question.choice_set.all() ，将会返回一个可迭代的 Choice 对象，这一对象可以在 {% for %} 标签内部使用。

### 去除模板中的url硬编码
我们在 polls/index.html 里编写投票链接时，链接是硬编码的

`<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>`

问题在于，硬编码和强耦合的链接，对于一个包含很多应用的项目来说，修改起来是十分困难的。然而，因为你在 polls.urls 的 url() 函数中通过 name 参数为 URL 定义了名字，你可以使用 {% url %} 标签代替它

`<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>`

这个标签的工作方式是在 polls.urls 模块的 URL 定义中寻具有指定名字的条目

如果你想改变投票详情视图的 URL，比如想改成 polls/specifics/12/ ，你不用在模板里修改任何东西（包括其它模板），只要在 polls/urls.py 里稍微修改一下就行

`path('specifics/<int:question_id>/', views.detail, name='detail'),`


## 表单

### 编写一个简单的表单

让我们更新一下投票详细页面的模板 ("polls/templates/polls/detail.html") ，让它包含一个 HTML `<form>`元素：

```html
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
{% endfor %}
<input type="submit" value="投票">
</form>
```

+ 上面的模板在 Question 的每个 Choice 前添加一个单选按钮。 每个单选按钮的 value 属性是对应的各个 Choice 的 ID。每个单选按钮的 name 是 "choice" 。这意味着，当有人选择一个单选按钮并提交表单提交时，它将发送一个 POST 数据 choice=# ，其中# 为选择的 Choice 的 ID。这是 HTML 表单的基本概念。
+ 我们设置表单的 action 为 {% url 'polls:vote' question.id %} ，并设置 method="post" 。使用 method="post"``（与其相对的是 ``method="get"`）是非常重要的，因为这个提交表单的行为会改变服务器端的数据。 
+ forloop.counter 指示 for 标签已经循环多少次。
+ 由于我们创建一个 POST 表单（它具有修改数据的作用），所以我们需要小心跨站点请求伪造。 所有针对内部 URL 的 POST 表单都应该使用 {% csrf_token %} 模板标签。

### vote() 视图

```python
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question
# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 重新显示投票表单
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "选择错误",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 重定向到结果页面
        return HttpResponseRedirect(reverse('results', args=(question.id,)))
```


+ request.POST 是一个类字典对象，让你可以通过关键字的名字获取提交的数据。 这个例子中， request.POST['choice'] 以字符串形式返回选择的 Choice 的 ID。 request.POST 的值永远是字符串。

注意，Django 还以同样的方式提供 request.GET 用于访问 GET 数据

+ 如果在 request.POST['choice'] 数据中没有提供 choice ， POST 将引发一个 KeyError 。上面的代码检查 KeyError ，如果没有给出 choice 将重新显示 Question 表单和一个错误信息。

+ 在增加 Choice 的得票数之后，代码返回一个 HttpResponseRedirect 而不是常用的 HttpResponse 、 HttpResponseRedirect 只接收一个参数：用户将要被重定向的 URL（请继续看下去，我们将会解释如何构造这个例子中的 URL）。

+ 我们在 HttpResponseRedirect 的构造函数中使用 reverse() 函数。这个函数避免了我们在视图函数中硬编码 URL。它需要我们给出我们想要跳转的视图的名字和该视图所对应的 URL 模式中需要给该视图提供的参数。  reverse() 调用将返回一个这样的字符串 `'/polls/1/results/'` 其中 1 是 question.id 的值。重定向的 URL 将调用 'results' 视图来显示最终的页面。

###  result() 视图

 vote() 视图将请求重定向到 Question 的结果界面。让我们来更新这个视图
 ```python
 def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

 ```
 现在，创建一个 polls/templates/polls/results.html 模板
 ```
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} 票</li>
{% endfor %}
</ul>

<a href="{% url 'detail' question.id %}">再次投票?</a>
 ```
 现在，在你的浏览器中访问 /polls/1/ 然后为 Question 投票。你应该看到一个投票结果页面，并且在你每次投票之后都会更新。