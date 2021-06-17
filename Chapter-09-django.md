# django
[toc]
## 单元测试

### 开始第一个测试
将下面的代码写入polls/tests.py

```
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() 返回 False 如果问题是一天前创建的
        """
        time = timezone.now() - datetime.timedelta(days=2)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```

我们创建了一个 django.test.TestCase 的子类，并添加了一个方法，此方法创建一个 pub_date 为两天前 Question 实例。然后检查它的 was_published_recently() 方法的返回值——它 应该 是 False。

### 运行测试
执行下命令运行测试
` python manage.py test polls`

输出结果如下
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
(venv) PS D:\python\python-dev\Chapter-08-code\mysite> python manage.py test polls
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...
```

以下是自动化测试的运行过程:
+ python manage.py test polls 将会寻找 polls 应用里的测试代码
+ 它找到了 django.test.TestCase 的一个子类
+ 它创建一个特殊的数据库供测试使用
+ 它在类中寻找测试方法——以 test 开头的方法。
+ 在 test_was_published_recently_with_future_question 方法中，它创建了一个 pub_date 值为 2天前的 Question 实例。
+ 接着使用 assertls() 方法，发现 was_published_recently() 返回了 False，而我们期望它返回 False。

### 测试视图

Django 提供了一个供测试使用的 Client 来模拟用户和视图层代码的交互。我们能在 tests.py 甚至是 shell 中使用它。

执行命令进入django shell

`python.exe manage.py shell`

```
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
```
配置测试环境

```
>>> from django.test import Client  
>>> client = Client()
>>> response = client.get('/') 
Not Found: /
>>> response = client.get('/polls/')
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#39;s new?</a></li>\n    \n    </ul>\n'
>>> from django.urls import reverse
>>> response = client.get(reverse('index'))
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#39;s new?</a></li>\n    \n    </ul>\n'
>>> response.context['latest_question_list']
<QuerySet [<Question: What's new?>]>
```

将下面的代码添加到 polls/tests.py

`from django.urls import reverse`

然后我们写一个函数用于创建投票问题，再为视图创建一个测试类
```
def create_question(question_text, days):
    """
    创建一个Question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        questions不存在
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        question存在
        """
        create_question(question_text="去哪儿玩", days=-1)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: 去哪儿玩>']
        )
```

测试详情视图

```
class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
```

## 静态文件
除了服务端生成的 HTML 以外，网络应用通常需要一些额外的文件——比如图片，脚本和样式表——来帮助渲染网络页面。在 Django 中，我们把这些文件统称为“静态文件”。

### 自定义样式
首先，在你的 polls 目录下创建一个名为 static 的目录。Django 将在该目录下查找静态文件，这种方式和 Diango 在 polls/templates/ 目录下查找 template 的方式类似。

django会在每个 INSTALLED_APPS 中指定的应用的子文件中寻找名称为 static 的特定文件夹

在你刚创建的 static 文件夹中创建一个名为 polls 的文件夹，再在 polls 文件夹中创建一个名为 style.css 的文件。你的样式表路径应是 polls/static/polls/style.css

将以下代码放入样式表(polls/static/polls/style.css)：
```
li a {
    color: green;
}
```

下一步，在 polls/templates/polls/index.html 的文件头添加以下内容：
```
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}" />
```

{% static %} 模板标签会生成静态文件的绝对路径。
重新访问 http://127.0.0.1:8000/polls/ 然后你可以看到投票链接是绿色的，这意味着你的样式表被正确加载了。

### 添加一个背景图

我们会创建一个用于存在图像的目录。在 polls/static/polls 目录下创建一个名为 images 的子目录。在这个目录中，放一张名为 background.gif 的图片。换言之，在目录 polls/static/polls/images/background.png 中放一张图片。

随后，polls/static/polls/style.css中添加：
```
body {
    background: white url("images/background.png") no-repeat;
}
```

## 模板继承

几乎每个网站都有一系列重复的组件，例如页头、侧边栏和页脚，但是每个页面都重复编写这些组件的 HTML 显然是不明智的。试想，如果要调整网站的页头呢？你要修改每个页面，换用新的页头。这是个费时的工作，而且可能出现人为错误。为免浪费时间复制粘贴 HTML 标记，我们可以利用 Django 模板引擎提供的模板继承功能尽量避免重复。使用模板继承的基本步骤如下：

1. 找出模板中重复出现的部分，例如页头、侧边栏、页脚和内容区。有时，你可以把各页面的结构画在纸上，这样便于找出通用的部分。
3. 创建一个基模板（ base template），实现页面的基本骨架结构，提供通用的部分（例如页头的徽标和标题，页脚的版权声明），并定义一些区块（ block），以便在不同的页面调整所显示的内容。
4. 为应用的不同页面创建专门的模板，都继承自基模板，然后指定各区块的内容

### 定义base模板

创建一个base模板
polls/templates/polls/base.html
```
<!DOCTYPE html>
<html>
  <head lang="zh">
    <meta charset="UTF-8" />
    <title>投票</title>
  </head>
  <body>
    <!-- 各页面的具体内容 -->
  </body>
</html>
```

### 定义block
创建好基础模板之后，接下来要指明模板中的哪些部分可由继承它的模板覆盖。为此，要使用`block`标签。例如，可以像下面这样在 base.html 模板中添加

```
<!DOCTYPE html>
<html>
  <head lang="zh">
    <meta charset="UTF-8" />
    <title>投票</title>
  </head>
  <body>
    {% block body_block %}
    {% endblock %}
  </body>
</html>
```

Django 模板标签放在 {% 和 %} 之间。因此，区块以 {% block %} 开头，其中 是区块的名称。区块必须以 endblock 结尾，而且也要放在 {% 和 %} 之间，即 {% endblock %}。

可以为区块指定默认内容，在子模板没有提供该区块的内容时使用。指定默认内容的方法是在 {% block %} 和 {% endblock %} 之间添加 HTML 标记，如下所示。
```
    {% block body_block %}
      这是区块默认内容
    {% endblock %}
```
创建各页面的模板时，我们将继承 polls/templates/polls/base.html模板，然后覆盖 body_block 区块的内容。模板中的区块数量不限，可以根据需要定义。例如，可以创建页面标题区块、页脚区块、侧边栏block，等等。block是 Django 模板系统一个特别强大的功能。

### index.html使用模板
```
{% extends 'polls/base.html' %}
{% block body_block %}
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}" />
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
{% endblock  %}
```

练习：将detail.html模板继承base.html

## template 概念

作为一个Web框架，Django需要一种动态生成HTML的便捷方法。最常用的方法依赖于模板。模板包含所需HTML输出的静态部分以及描述动态内容将被插入的一些特殊语法。

### 变量

变量看起来就像是这样： `{{ variable }}`

当模版引擎遇到一个变量，它将从上下文context中获取这个变量的值，然后用值替换掉它本身。

当模版系统渲染变量的时候遇到点(".")，它将以这样的顺序查询这个圆点具体代表的功能：

字典查询（Dictionary lookup）
属性或方法查询（Attribute or method lookup）
如果你使用的变量不存在，模版系统将插入string_if_invalid选项的值，默认设置为''(空字符串)。

### 标签

标签看起来像是这样的： {% tag %}。

标签比变量复杂得多，有些用于在输出中创建文本，有些用于控制循环或判断逻辑，有些用于加载外部信息到模板中供以后的变量使用。

一些标签需要开始和结束标签（即 {％ 标签 ％} ... 标签 内容 ... {％ ENDTAG ％}）。

下面是一些常用的标签：

1.  for循环标签
```
{% for question in latest_question_list %}
        <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
{% endfor %}
```

2. if，elif和else标签
```
{% if 条件1 %}
    .....
{% elif 条件2 %}
    .....
{% else %}
    ......
{% endif %}
```

3. block和extends标签
继承模板

4. csrf_token标签
该标签用来防止跨站请求伪造

### 注释

要注释模版中一行的部分内容，使用注释语法:{# #}。

`{# greeting #}`

以上是单行注释（在{# .... #}中，不允许有新行）

commnet 标签多行注释
```
{% comment "Optional note" %}
    <p>行1</p>
    <p>行2</p>
{% endcomment %}
```

### 过滤器

过滤器看起来是这样的：{{ name | lower }}。使用管道符号(|)来应用过滤器。该过滤器将文本转换成小写。

一些过滤器带有参数。 过滤器的参数看起来像是这样： {{ bio|truncatewords:30 }}。 这将显示bio变量的前30个词。

过滤器参数包含空格的话，必须用引号包起来。例如，使用逗号和空格去连接一个列表中的元素，你需要使用{{ list|join:", "}}。

下面是一些常用的模版过滤器：
1. default
为false或者空变量提供默认值，像这样：

`{{ value|default:"nothing" }}`
2. length
返回值的长度。它对字符串和列表都起作用。

`{{ value|length }}`
如果value是`['a', 'b', 'c', 'd']`，那么输出4。

3. filesizeformat
格式化为“人类可读”文件大小单位（即'13 KB'，4.1 MB'，'102 bytes'等）。

`{{ value|filesizeformat }}`
如果value是123456789，输出将会是117.7MB。

我们可以创建自定义的模板过滤器和标签



## 登录注册app

创建login app

`python manage.py startapp login`


### 设计数据模型
模型中定义了数据如何在数据库内保存，也就是数据表的定义方式。这部分工作体现在Django的代码中，其实就是model类的设计。

#### 数据库模型设计
作为一个用户登录和注册项目，需要保存的都是各种用户的相关信息。很显然，我们至少需要一张用户表User，在用户表里需要保存下面的信息：

用户名
密码
邮箱地址
性别
创建时间

编辑login/models.py文件，代码如下：

```
from django.db import models

# Create your models here.
class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
```
属性：
+ max_length：最长字符限制
+ unique: 内容唯一
+ default：默认值
+ auto_now_add: 插入数据时自动添加时间
+ choices: 选择项，插入时该字段内容必须为choices里包含的内容，choices为列表或元组，里面的每一项为元组

各字段含义：

+ name: 必填，最长不超过128个字符，并且唯一，也就是不能有相同姓名；
+ password: 必填，最长不超过256个字符（实际可能不需要这么长）；
+ email: 使用Django内置的邮箱类型，并且唯一；
+ sex: 性别，使用了一个choice，只能选择男或者女，默认为男；
+ 使用__str__方法帮助人性化显示对象信息；
+ 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；

### 注册app

每次创建了新的app后，都需要在全局settings中注册，这样Django才知道你有新的应用上线了。在INSTALLED_APPS部分添加`login.apps.LoginConfig`
mysiste/settings.py

```
INSTALLED_APPS = [
    'login.apps.LoginConfig',
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

生成migrations文件,执行以下命令

`python manage.py makemigrations`

输出如下
```
Migrations for 'login':
  login\migrations\0001_initial.py
    - Create model User
```

Django自动为我们创建了login\migrations\0001_initial.py文件，保存了我们的第一次数据迁移工作，也就是创建了User模型。

同步到数据库执行命令

`python manage.py migrate`

输出内容如下：
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, login, polls, sessions
Running migrations:
  Applying login.0001_initial... OK
```

### 在admin注册模型

编辑文件login/admin.py
```
from django.contrib import admin

from .models import User

admin.site.register(User)
```

然后进入admin后台查看
添加一个测试用户

### 路由和视图
前面我们已经创建好数据模型了，并且在admin后台中添加了一些测试用户。下面我们就要设计好站点的url路由、对应的处理视图函数以及使用的前端模板了。

#### 路由设计
URL	视图	模板	说明
/index/	login.views.index	index.html	主页
/login/	login.views.login	login.html	登录
/register/	login.views.register	register.html	注册
/logout/	login.views.logout	无需专门的页面	登出


+ 未登录人员，不论是访问index还是login和logout，全部跳转到login界面
+ 已登录人员，访问login会自动跳转到index页面
+ 已登录人员，不允许直接访问register页面，需先logout
+ 登出后，自动跳转到login界面

新建login/urls.py,内容如下
```
from django.urls import path
from . import  views
app_name = 'login'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout, name='logout'),
]
```
注意： 我们添加了个app_name 变量，这个是定义URLConf的命名空间，用来区别不同app下，相同的name
编辑mysite/urls.py添加`path('auth/', include('login.urls')),`

### 架构视图
```
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    pass
    return render(request, 'login/login.html')


def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    pass
    return redirect(reverse('login:login'))
```


注意：

在顶部额外导入了redirect，用于logout后，页面重定向到‘/login/’这个url，当然你也可以重定向到别的页面；
另外三个视图都返回一个render调用，render方法接收request作为第一个参数，要渲染的页面为第二个参数，以及需要传递给页面的数据字典作为第三个参数（可以为空），表示根据请求的部分，以渲染的HTML页面为主体，使用模板语言将数据字典填入，然后返回给用户的浏览器。
渲染的对象为login目录下的html文件，这是一种安全可靠的文件组织方式，我们现在还没有创建这些文件。

### 创建模板

在login目录中创建一个templates目录，再在templates目录里创建一个login目录。既login/templates/login

在login/templates/login目录中创建三个文件index.html、login.html以及register.html ，并写入如下的代码：

login/templates/login/index.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
<h1>这仅仅是一个主页模拟！请根据实际情况接入正确的主页！</h1>
</body>
</html>
```

login/templates/login/login.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>
<h1>登录页面</h1>
</body>
</html>
```

login/templates/login/register.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>注册</title>
</head>
<body>
<h1>注册页面</h1>
</body>
</html>
```

访问以下页面
+ http://127.0.0.1:8000/auth/login/
+ http://127.0.0.1:8000/auth/logout/
+ http://127.0.0.1:8000/auth/register/
+ http://127.0.0.1:8000/auth/index