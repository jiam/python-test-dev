## 前端页面设计

### 编写具体的login.html
login/templates/login/login.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>

    <div style="margin: 15% 40%;">
        <h1>欢迎登录！</h1>
       <form action={% url 'login:login' %} method="post">
            {% csrf_token %}
            <p>
                <label for="id_username">用户名：</label>
                <input type="text" id="id_username" name="username" placeholder="用户名" autofocus required />
            </p>
            <p>
                <label for="id_password">密码：</label>
                <input type="password" id="id_password" placeholder="密码" name="password" required >
            </p>
            <input type="submit" value="确定">
        </form>
    </div>

</body>
</html>
```

+ form标签主要确定目的地url和发送方法；
+ p标签将各个输入框分行；
+ label标签为每个输入框提供一个前导提示，还有助于触屏使用；
+ placeholder属性为输入框提供占位符；
+ autofocus属性为用户名输入框自动聚焦
+ required表示该输入框必须填写
+ passowrd类型的input标签不会显示明文密码

浏览器打开http://127.0.0.1:8000/auth/login/查看

引入bootstrap

```html
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- 上述meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <!-- Bootstrap CSS -->
    <link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <title>登录</title>
  </head>
  <body>
    <div class="container">
            <div class="col">
              <form class="form-login" action={% url 'login:login' %} method="post">
                  {% csrf_token %}
                  <h3 class="text-center">欢迎登录</h3>
                  <div class="form-group">
                    <label for="id_username">用户名：</label>
                    <input type="text" name='username' class="form-control" id="id_username" placeholder="Username" autofocus required>
                  </div>
                  <div class="form-group">
                    <label for="id_password">密码：</label>
                    <input type="password" name='password' class="form-control" id="id_password" placeholder="Password" required>
                  </div>
                <div>
                  <a href="/register/" class="text-success "><ins>新用户注册</ins></a>
                  <button type="submit" class="btn btn-primary float-right">登录</button>
                </div>
              </form>
            </div>
    </div> <!-- /container -->

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    {#    以下三者的引用顺序是固定的#}
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.15.0/umd/popper.js"></script>
    <script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>

  </body>
</html>
```

+ CSS：`<link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">`
+ JS：`<script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>`

### 调整登录页样式

创建目录`static\login\css`和`static\login\image`

创建`static\login\css\login.css`,将bg.jgp 放入`static\login\image\bg.jpg`

```css
body {
  height: 100%;
  background-image: url('../image/bg.jpg');
}
.form-login {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: 0 auto;
}
.form-login{
  margin-top:80px;
  font-weight: 400;
}
.form-login .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;

}
.form-login .form-control:focus {
  z-index: 2;
}
.form-login input[type="text"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-login input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
form a{
  display: inline-block;
  margin-top:25px;
  font-size: 12px;
  line-height: 10px;
}
```

在login.html最上面添加`{% load static %}`
head 部分田间`<link href="{% static 'login/css/login.css' %}" rel="stylesheet"/>`

重启runserver，然后浏览登录页面


## 登录视图

### login 
根据我们在路由中的设计，用户通过login.html中的表单填写用户名和密码，并以POST的方式发送到服务器的/login/地址。服务器通过login/views.py中的login()视图函数，接收并处理这一请求。


我们可以通过下面的方法接收和处理请求：
login/views.py
```python
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        return redirect('login:index')
    return render(request, 'login/login.html')
```

+ request.method中封装了数据请求的方法，如果是“POST”（全大写），将执行if语句的内容，如果不是，直接返回最后的render()结果，也就是正常的登录页面；
+ request.POST封装了所有POST请求中的数据，这是一个字典类型，可以通过get方法获取具体的值。类似get('username')中的键‘username’是HTML模板中表单的input元素里‘name’属性定义的值。所以在编写form表单的时候一定不能忘记添加name属性。
+ 利用redirect方法，将页面重定向到index页。

注意这里我们只是print了下账号密码，并没有验证

### 验证数据

对用户发送的数据进行验证。数据验证分前端页面验证和后台服务器验证。前端验证可以通过专门的插件或者自己写JS代码实现，也可以简单地使用HTML5的新特性。这里，我们使用的是HTML5的内置验证功能。
查看我们的login/templstes/login/login.html
```html
                  <div class="form-group">
                    <label for="id_username">用户名：</label>
                    <input type="text" name='username' class="form-control" id="id_username" placeholder="Username" autofocus required>
                  </div>
                  <div class="form-group">
                    <label for="id_password">密码：</label>
                    <input type="password" name='password' class="form-control" id="id_password" placeholder="Password" required>
                  </div>
```
上面的required 属性要求该字段必须填写，否则不能提交

前端页面的验证都是用来给守法用户做提示和限制的，并不能保证绝对的安全，后端服务器依然要重新对数据进行验证。

编辑 login/views.py，首先导入User模型类

`from .models import User`

然后修改login函数
```python
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:  # 确保用户名和密码都不为空
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = User.objects.get(name=username)
            except:
                return render(request, 'login/login.html')
            if user.password == password:
                return redirect('login:index')
    return render(request, 'login/login.html')
```

打开登录页面，如果账号密码正确才会跳转到index页面，注意这里还有问题，账号密码错误没有提示信息

### 添加提示信息

上面的代码还缺少很重要的一部分内容，也就是错误提示信息！无论是登录成功还是失败，用户都没有得到任何提示信息

再次修改login/views.py 中的login函数
```python
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        if username.strip() and password:
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', {'message': message})

            if user.password == password:
                print(username, password)
                return redirect('login:index')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', {'message': message})
        else:
            return render(request, 'login/login.html', {'message': message})
    return render(request, 'login/login.html')
```
注意在redner的上下文参数中我们定义了message变量



这里增加了message变量，用于保存提示信息。当有错误信息的时候，将错误信息打包成一个字典，然后作为第三个参数提供给render方法。这个数据字典在渲染模板的时候会传递到模板里供你调用。

为了在前端页面显示信息，还需要对login.html进行修改：

```html
              <form class="form-login" action={% url 'login:login' %} method="post">
                  {% if message %}
                    <div class="alert alert-warning">{{ message }}</div>
                  {% endif %}
                  {% csrf_token %}
                  <h3 class="text-center">欢迎登录</h3>
                  <div class="form-group">
                    <label for="id_username">用户名：</label>
                    <input type="text" name='username' class="form-control" id="id_username" placeholder="Username" autofocus required>
                  </div>
                  <div class="form-group">
                    <label for="id_password">密码：</label>
                    <input type="password" name='password' class="form-control" id="id_password" placeholder="Password" required>
                  </div>
                <div>
                  <a href="/register/" class="text-success "><ins>新用户注册</ins></a>
                  <button type="submit" class="btn btn-primary float-right">登录</button>
                </div>
              </form>
```

在form里添加
```html
                  {% if message %}
                    <div class="alert alert-warning">{{ message }}</div>
                  {% endif %}
```
通过判断message变量是否为空，也就是是否有错误提示信息，如果有，就显示出来！这里使用了Bootstrap的警示信息类alert

再次测试登录页面

## django 表单

我们前面都是手工在HTML文件中编写表单form元素，然后在views.py的视图函数中接收表单中的用户数据，再编写验证代码进行验证，最后使用ORM进行数据库的增删改查。这样费时费力，整个过程比较复杂，而且有可能写得不太恰当，数据验证也比较麻烦。设想一下，如果我们的表单拥有几十上百个数据字段，有不同的数据特点，如果也使用手工的方式，其效率和正确性都将无法得到保障。有鉴于此，Django在内部集成了一个表单功能，以面向对象的方式，直接使用Python代码生成HTML表单代码，专门帮助我们快速处理表单相关的内容

Django的表单给我们提供了下面三个主要功能：

+ 准备和重构数据用于页面渲染；
+ 为数据创建HTML表单元素；
+ 接收和处理用户从表单发送过来的数据。

编写Django的form表单，非常类似我们在模型系统里编写一个模型。在模型中，一个字段代表数据表的一列，而form表单中的一个字段代表`<form>`中的一个`<input>`元素。

### 创建表单模型

在login文件夹下，新建一个forms.py文件，也就是login/forms.py

```python
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)
```
+ 顶部要先导入forms模块 所有的表单类都要继承forms.Form类
+ 每个表单字段都有自己的字段类型比如CharField，它们分别对应一种HTML语言中`<form>`内的一个input元素。这一点和Django模型系统的设计非常相似。
+ label参数用于设置`<label>`标签
+ max_length限制字段输入的最大长度。它同时起到两个作用，一是在浏览器页面限制用户输入不可超过字符数，二是在后端服务器验证用户输入的长度也不可超过。
+ widget=forms.PasswordInput用于指定该字段在form表单里表现为`<input type='password' />`，也就是密码输入框。

### 修改login 视图函数

使用了Django的表单后，就要在视图中进行相应的修改 login/views.py:

首先在文件头部导入UserForm

`from .forms import UserForm`

然后修改login函数
```python
def login(request):
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == password:
                return redirect('login:index')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())
```

+ 在顶部要导入我们写的forms模块:from . import forms
+ 对于POST方法，接收表单数据，并验证；
+ 使用表单类自带的is_valid()方法一步完成数据验证工作；
+ 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值；
+ 如果验证不通过，则返回一个包含先前数据的表单给前端页面，方便用户修改。也就是说，它会帮你保留先前填写的数据内容，而不是返回一个空表！
+ 对于非POST方法发送数据时，比如GET方法请求页面，返回空的表单，让用户可以填入数据；

另外，这里使用了一个小技巧，Python内置了一个locals()函数，它返回当前所有的本地变量字典，我们可以偷懒的将这作为render函数的数据字典参数值，就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了

### 修改登录页面
Django的表单很重要的一个功能就是自动生成HTML的form表单内容。现在，我们需要修改一下原来的login/templates/lgon/login.html文件：
将form部分替换为下面内容

```html
                <form class="form-login" action={% url 'login:login' %}  method="post">
                  {% if message %}
                    <div class="alert alert-warning">{{ message }}</div>
                  {% endif %}
                  {% csrf_token %}
                  <h3 class="text-center">欢迎登录</h3>

                  {{ login_form }}

                  <div>
                      <a href={% url 'login:register' %} class="text-success " ><ins>新用户注册</ins></a>
                      <button type="submit" class="btn btn-primary float-right">登录</button>
                  </div>
                </form>
```

+ {{ login_form }}完成了表单内容的生成工作，login_form这个名称来自你在视图函数中生成的form实例的变量名，但是，它不会生成`<form>...</form>`标签，这个要自己写；
+ Django自动为每个input元素设置了一个id名称，对应label的for参数

我们可以到浏览器中，看下实际生成的html源码是什么

Django的form表单功能，帮你自动生成了下面部分的代码
```html

<tr><th><label for="id_username">用户名:</label></th><td><input type="text" name="username" value="fdsfs" maxlength="128" required id="id_username"></td></tr>
<tr><th><label for="id_password">密码:</label></th><td><input type="password" name="password" maxlength="256" required id="id_password"></td></tr>
```
这就是一个table，而且是不带`<table></table>`

实际上除了通过{{ login_form }}简单地将表单渲染到HTML页面中了，还有下面几种方式：

{{ login_form.as_table }} 将表单渲染成一个表格元素，每个输入框作为一个`<tr>`标签
{{ login_form.as_p }} 将表单的每个输入框包裹在一个`<p>`标签内
{{ login_form.as_ul }} 将表单渲染成一个列表元素，每个输入框作为一个`<li>`标签


### 手动渲染表单字段

可以通过{{ login_form.name_of_field }}获取每一个字段，然后分别渲染，如下例所示

```html
<div class="form-group">
  {{ login_form.username.label_tag }}
  {{ login_form.username}}
</div>
<div class="form-group">
  {{ login_form.password.label_tag }}
  {{ login_form.password }}
</div>
```
再次查看login页面，还是跟我们以前的不一样，因为缺少了input元素里少了form-control的class，以及placeholder和autofocus

修改login/forms.py 添加attrs属性
```python
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))
```
再次查看login页面

## 图片验证码
为了防止机器人频繁登录网站或者破坏分子恶意登录，很多用户登录和注册系统都提供了图形验证码功能。
在Django中实现图片验证码功能非常简单，有现成的第三方库可以使用，我们不必自己开发（也要能开发得出来，囧）。这个库叫做django-simple-captcha。

### 安装captcha

执行命令`pip install django-simple-captcha`

### 注册captcha
在settings中，将‘captcha’注册到app列表里
```python
INSTALLED_APPS = [
    'captcha',
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

captcha需要在数据库中建立自己的数据表，所以需要执行migrate命令生成数据表：

`python manage.py migrate`

### 添加路由
修改根URLConf
```python
urlpatterns = [
    path('polls/', include('polls.urls')),
    path('auth/', include('login.urls')),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls'))
]
```

### 修改login/forms.py

添加图片验证码字段
```python
from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control',  'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')
```
注意需要提前导入from captcha.fields import CaptchaField，然后就像写普通的form字段一样添加一个captcha字段就可以了！

### 修改login.html页面
添加验证码部分
```html
                  <div class="form-group">
                    {{ login_form.captcha.label_tag }}
                    {{ login_form.captcha }}
                  </div>
```
打开登录页面查看


## session

因为因特网HTTP协议的特性，每一次来自于用户浏览器的请求（request）都是无状态的、独立的。通俗地说，就是无法保存用户状态，后台服务器根本就不知道当前请求和以前及以后请求是否来自同一用户。对于静态网站，这可能不是个问题，而对于动态网站，尤其是京东、天猫、银行等购物或金融网站，无法识别用户并保持用户状态是致命的，根本就无法提供服务。你可以尝试将浏览器的cookie功能关闭，你会发现将无法在京东登录和购物。

为了实现连接状态的保持功能，网站会通过用户的浏览器在用户机器内被限定的硬盘位置中写入一些数据，也就是所谓的Cookie。通过Cookie可以保存一些诸如用户名、浏览记录、表单记录、登录和注销等各种数据。但是这种方式非常不安全，因为Cookie保存在用户的机器上，如果Cookie被伪造、篡改或删除，就会造成极大的安全威胁，因此，现代网站设计通常将Cookie用来保存一些不重要的内容，实际的用户数据和状态还是以Session会话的方式保存在服务器端。

但是，必须清楚的是Session依赖Cookie！不同的地方在于Session将所有的数据都放在服务器端，用户浏览器的Cookie中只会保存一个非明文的识别信息，比如哈希值。

Django提供了一个通用的Session框架，并且可以使用多种session数据的保存方式：
+ 保存在数据库内
+ 保存到缓存
+ 保存到文件内

Django的session框架默认启用，并已经注册在app设置内了既`django.contrib.sessions`

### 使用session

修改login/views.py 
```python
def login(request):
    if request.session.get('is_login',None):
        return redirect("login:index")
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('login:index')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())
```

通过下面的if语句，我们不允许重复登录
```python
if request.session.get('is_login',None):
    return redirect("login:index")
```

通过下面的语句，我们往session字典内写入用户状态和数据：
```
request.session['is_login'] = True
request.session['user_id'] = user.id
request.session['user_name'] = user.name
```

既然有了session记录用户登录状态，那么就可以完善我们的登出视图函数了：
```python
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("login:login")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("login:login")
```

flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。

### 在index页面中验证登录

有了用户状态，就可以根据用户登录与否，展示不同的页面，比如在index页面中显示当前用户的名称：

修改index.html的代码：
```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
<h1>{{ request.session.user_name }}!  欢迎回来！</h1>
<p>
    <a href={% url 'login:logout' %}>登出</a>
</p>
</body>
</html>
```

注意即使退出后，我们仍然可以直接访问index页面，因为index函数还未添加登录限制

修改index视图函数，添加相关限制：
```python
def index(request):
    if not request.session.get('is_login', None):
        return redirect('login:login')
    return render(request, 'login/index.html')
```
再次访问index页面，如果未登录就会跳转到login页面

## 注册视图

实现注册功能

### 创建forms

显而易见，我们的注册页面也需要一个form表单。同样地，在/login/forms.py中添加一个新的表单类

```python
class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')
```

### 完善register.html
同样地，类似login.html文件，我们手工在register.html中编写forms相关条目：

```html
{% load static %}
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- 上述meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <!-- Bootstrap CSS -->
    <link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'login/css/register.css' %}" rel="stylesheet"/>
    <title>注册</title>
  </head>
  <body>
    <div class="container">
            <div class="col">
                <form class="form-register" action={% url 'login:register' %} method="post">

                    {% if register_form.captcha.errors %}
                        <div class="alert alert-warning">{{ register_form.captcha.errors }}</div>
                    {% elif message %}
                        <div class="alert alert-warning">{{ message }}</div>
                    {% endif %}

                  {% csrf_token %}
                  <h3 class="text-center">欢迎注册</h3>

                  <div class="form-group">
                      {{ register_form.username.label_tag }}
                      {{ register_form.username}}
                  </div>
                  <div class="form-group">
                      {{ register_form.password1.label_tag }}
                      {{ register_form.password1 }}
                  </div>
                  <div class="form-group">
                      {{ register_form.password2.label_tag }}
                      {{ register_form.password2 }}
                  </div>
                  <div class="form-group">
                      {{ register_form.email.label_tag }}
                      {{ register_form.email }}
                  </div>
                  <div class="form-group">
                      {{ register_form.sex.label_tag }}
                      {{ register_form.sex }}
                  </div>
                  <div class="form-group">
                      {{ register_form.captcha.label_tag }}
                      {{ register_form.captcha }}
                  </div>

                  <div>
                      <a href={% url 'login:login' %}  ><ins>直接登录</ins></a>
                      <button type="submit" class="btn btn-primary float-right">注册</button>
                  </div>
                </form>
            </div>
    </div> <!-- /container -->

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    {#    以下三者的引用顺序是固定的#}
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.15.0/umd/popper.js"></script>
    <script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>

  </body>
</html>
```

编写register.css样式文件

```css
body {
height: 100%;
background-image: url('../image/bg.jpg');
}
.form-register {
width: 100%;
max-width: 400px;
padding: 15px;
margin: 0 auto;
}
.form-group {
margin-bottom: 5px;
}
form a{
display: inline-block;
margin-top:25px;
line-height: 10px;
}
```

### 实现注册视图

打开login/views.py文件，现在来完善我们的register()

```python
def register(request):
    if request.session.get('is_login', None):
        return redirect('login:index')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('login:login')
        else:
            return render(request, 'login/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())
```


从大体逻辑上，也是先实例化一个RegisterForm的对象，然后使用is_valide()验证数据，再从cleaned_data中获取数据。

重点在于注册逻辑，首先两次输入的密码必须相同，其次不能存在相同用户名和邮箱，最后如果条件都满足，利用ORM，创建一个用户实例，然后保存到数据库内。

对于注册的逻辑，不同的生产环境有不同的要求，请跟进实际情况自行完善，这里只是一个基本的注册过程，不能生搬照抄。

尝试注册

### 加密密码

首先在login/views.py中编写一个hash函数

```python
import hashlib

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
```

修改login函数

```python
if user.password == hash_code(password):
    request.session['is_login'] = True
    request.session['user_id'] = user.id
    request.session['user_name'] = user.name
    return redirect('login:index')
```

修改register函数

```python
new_user = User()
new_user.name = username
new_user.password = hash_code(password1)
new_user.email = email
new_user.sex = sex
new_user.save()
```

删除原有用户，注册新用户并登录