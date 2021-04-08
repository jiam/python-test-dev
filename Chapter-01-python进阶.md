# python进阶
[toc]
## 装饰器 

装饰器是可调用的对象，其参数是另一个函数（被装饰的函数），装饰器可以处理被装饰的函数，然后把它返回一个函数

将target替换为inner
````python
def deco(func):
    def inner():
        print("running inner()")
    return inner

@deco
def target():
    print('running target()')


if __name__ == "__main__":
    target()

````
等效
````python
def deco(func):
    def inner():
        func()
        print("running inner()")
    return inner


def target():
    print('running target()')


if __name__ == "__main__":
    target = deco(target)
    target()

````


它可以让被装饰的函数在不需要做任何代码变动的前提下增加额外的功能，
我们需要记住装饰器的几点属性，以便后面能更好的理解

+ 实质： 是一个函数
+ 参数：被装饰函数名
+ 返回：返回一个函数
+ 作用：为已经存在的对象添加额外的功能



调用被装饰函数时,参数传递给返回的函数，所以wrap的参数要与被装饰函数一致，或者写成wrap(*arg, **dict)
````python
def add_decorator(f):
    def wrap(x,y):
        print("加法")
        return f(x,y)
    return wrap

@add_decorator
def add_method(x, y):
    return x + y


print(add_method(2,3))
````
统计函数的执行时间
````python
import time

def decorator(func):
    def wrapper(*arg, **kwarg):
        start_time = time.time()
        r = func(*arg, **kwarg)
        end_time = time.time()
        print("执行时间:",end_time - start_time)
        return r
    return wrapper

@decorator
def func():
    time.sleep(1)
    return "hello world"

print(func())
````


## 可迭代的对象，迭代器
迭代的意思是重复做一些事很多次，for循环就是一种迭代，字符串、列表、字典，元组都是可迭代对象
实现__iter__方法的对象都是可迭代的对象。 `__iter__` 返回一个迭代器，所谓迭代器就是具有 `__next__`方法的对象
在掉用next方法的时，迭代器会返回它的下一个值，如果没有值了，则返回StopIteration
````python
>>> li = [1,2,3]   # li为可迭代对象
>>> b = li.__iter__()    #b 为迭代器
>>> next(b)
1
>>> next(b)
2
>>> next(b)
3
>>> next(b)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
````
python内置函数next(obj) 等于 obj.__next__,内置函数iter等于obj.__iter__

## 生成器
1. 生成器函数
生成器就是一种函数，跟普通函数不同的是，生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器。
生成器函数用来产生一个迭代器
yield语句挂起生成器函数并向调用者发送一个值，迭代器的_next__继续运行函数

````python
def number():
    i = 0
    while True:
        i += 1
        yield i

n = number()
print(next(n))
print(next(n))
for i in range(10):
    print(next(n))
````

前n个数求和
````python
def addsum(n):
    s = 0
    for i in range(1,n+1):
        s += i
        yield s

t = addsum(5)

while True:
    try:
        print(next(t))
    except StopIteration:
        break
````

2. 生成器表达式
````python
>>> f = ( x ** 2 for x in range(4))
>>> next(f)
0
>>> next(f)
1
>>> next(f)
4
>>> next(f)
9
````

##  序列化
我们把对象从内存中变成可存储或传输的字节码过程称之为序列化。序列化之后，就可以把序列化后的内容写入磁盘，或者通过网络传输到别的机器上。
反过来，把内容从序列化的字节码重新读到内存里称之为反序列化

### pickle
pickle模块是一种的对象序列化工具；对于内存中几乎任何的python对象，都能把对象转化为字节，
这个字节可以随后用来在内存中重建最初的对象。pickle模块能够处理我们用的任何对象，列表，字典
嵌套组合以及类和实例

#### dumps和 loads
列表对象
````
>>> import pickle
>>> l = [1,2,3]
>>> pickle.dumps(l)
b'\x80\x03]q\x00(K\x01K\x02K\x03e.'
>>> b = pickle.dumps(l)
>>> b
b'\x80\x03]q\x00(K\x01K\x02K\x03e.'
>>> pickle.loads(b)
````

字典对象
````
>>> d = {"id":1, "name": "贾敏强", "phone_number":"15801396646"}
>>> pickle.dumps(d)
b'\x80\x03}q\x00(X\x02\x00\x00\x00idq\x01K\x01X\x04\x00\x00\x00nameq\x02X\t\x00\x00\x00\xe8\xb4\xbe\xe6\x95\x8f\xe5\xbc\xbaq\x03X\x0c\x00\x00\x00phone_numberq\x04X\x0b\x00\x00\x0015801396646q\x05u.'
>>> b = pickle.dumps(d)
>>> pickle.loads(b)
{'id': 1, 'name': '贾敏强', 'phone_number': '15801396646'}
````

## 系统编程

### 文件操作

os 模块
1.  返回当前目录
`os.getcwd()`
2.  列出目录的内容
` os.listdir()`
3. 创建目录
`os.mkdir("te")`
4.  删除空目录
`os.rmdir("te")`
5. 重命名
`os.rename('1.py','2.py')`
6.  删除文件
`os.remove('2.py')`
9. 遍历目录中的所有文件
`os.walk` 返回一个3元组生成器
当前目录的名称，当前目录中子目录的列表，当前目录中文件的列表
````
import os

g = os.walk("d:/py/peixun/python-dev")
print(next(g))
print(next(g))
````


os.path 模块
1. abspath()  将相对路径转化为绝对路径
`os.path.abspath(path)`
2. dirname()  获取完整路径当中的目录部分
`os.path.dirname("d:/1/test")`
3. basename()获取完整路径当中的主体部分
`os.path.basename("d:/1/test")`
4. split() 将一个完整的路径切割成目录部分和主体部分
`os.path.split("d:/1/test")`
5. join() 将2个路径合并成一个
`os.path.join("d:/1", "test")`
6. getsize()  获取文件的大小
`os.path.getsize(path)`
7. isfile() 检测是否是文件
`os.path.isfile(path)`
8. isdir()  检测是否是文件夹
`os.path.isdir(path)`

列出目录下包括子目录的所有文件
````python
import os

for dirpath, dirames, filenames  in os.walk("d:/py/peixun/python-dev"):
    print('[' + dirpath + ']')
    for filename in filenames:
        print(os.path.join(dirpath, filename))
````

### 调用系统命令

os.system

`os.system('dir')` 

成功执行返回0
`print(os.system('dir'))`
失败返回非0
`print(os.system('dir e:\\'))`


os.popen

`os.popen('dir')`

```python
import os
r = os.popen('dir')
print(r.read())
```
subprocess.run
返回命令执行结果和返回码

````python
import subprocess
r = subprocess.run('dir', stdout=subprocess.PIPE,shell=True)
print(r.stdout)
print(r.stdout.decode('gbk'))
print(r.returncode)
````

### 命令行参数

```python
import sys
args = sys.argv
print(args)
print(args[0],args[1])
```
注意: sys.argv 的返回值 是个list

### 环境变量

```python
import os

r = os.environ
print(r)
print(r["PATH"])
```

## 并发编程

### 线程
线程是中轻量级的进程，所有线程均在同一个进程中，共享全局内存，用于任务并行
###  常见线程用法
实例1 不同任务并发
```python
import threading
import time


def helloworld():
    time.sleep(2)
    print("helloworld")


t = threading.Thread(target=helloworld)
t.start()
print("main thread")

```
注意：这里有两个线程一个是主线程，一个是通过threading模块产生的t线程，
这里程序并没有阻塞在helloword函数，主线程和t线程同时运行


实例2 同种任务并行

````python
import threading
import time


def helloworld(id):
    time.sleep(2)
    print("thread %d helloworld" % id)


for i in range(5):
    t = threading.Thread(target=helloworld, args=(i,))
    t.start()
print("main thread")
````


###  进程

multiprocessing 解决python线程不能利用多核cpu的问题

```python
import os

from multiprocessing import Process

def whoami(label):
    msg = '%s: name:%s, pid:%s'
    print(msg % (label, __name__,os.getpid()))


if __name__ == '__main__':
    for i in range(5):
        p = Process(target=whoami, args=('child',))
        p.start()
```

### Future

concurrent.futures供了ThreadPoolExecutor和ProcessPoolExecutor两个类，都继承自Executor，
分别被用来创建线程池和进程池，接受max_workers参数，代表创建的线程数或者进程数。ProcessPoolExecutor的max_workers参数可以为空，程序会自动创建基于电脑cpu数目的进程数。

ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor
from urllib import request

url ="https://www.baidu.com"

def get_baidu():
    r = request.urlopen(url)
    print(r.code)


with ThreadPoolExecutor(max_workers=4) as executor:
    for i in range(100):
        executor.submit(get_baidu)

```

ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor
from urllib import request

url ="https://www.baidu.com"

def get_baidu():
    r = request.urlopen(url)
    print(r.code)


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        for i in range(100):
            executor.submit(get_baidu)

```

[推荐资料](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/)


##作业
1. 复制目录,拷贝目录a到a.bak
2. 编写一个pemit装饰器实现权限认证
```python
def test(info):
    if info.username == 'root' and info.passwd =='1223':
        print('你有权限')
    else:
        print('你没有权限')
        return 
    return "1,2,3" 


def test2(info):
    if info.username == 'root' and info.passwd=='1223':
        print('你有权限')
    else:
        print('你没有权限')
        return 
    return "4,5,6" 


@permit
def test2(info)
    return "4,5,6" 

@permit
def test(info)
    return "123"
   
实现permit装饰器对权限进行验证
```
3. 使用future 编写一个多线程压测程序并统计状态码个数既200,非200等http 状态码个数