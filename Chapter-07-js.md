# javascript
[toc]

## 基本语法

### 语句

下面的一行代码就是一个完整的赋值语句
`var x = 1;`

下面的一行代码是字符串
`'Hello, world'`

### 语句块
语句块是一组语句的集合，例如，下面的代码先做了一个判断，如果判断成立，将执行{...}中的所有语句：
```js
if (2 > 1) {
    x = 1;
    y = 2;
    z = 3;
}
```
注意花括号{...}内的语句具有缩进，通常是4个空格。缩进不是JavaScript语法要求必须的，但缩进有助于我们理解代码的层次，所以编写代码时要遵守缩进规则。

{...}还可以嵌套，形成层级结构：
```js
if (2 > 1) {
    x = 1;
    y = 2;
    z = 3;
    if (x < y) {
        z = 4;
    }
    if (x > y) {
        z = 5;
    }
}

```

### 注释

以//开头直到行末的字符被视为行注释，注释是给开发人员看到，JavaScript引擎会自动忽略：
```js
// 这是一行注释
alert('hello'); 
```

另一种块注释是用/*...*/把多行字符包裹起来，把一大“块”视为一个注释：
```
/* 从这里开始是块注释
仍然是注释
仍然是注释
注释结束 */
```

### 大小写
请注意，JavaScript与python一样区分大小写


### hello world

`alert("hello world")`

### 变量

变量在JavaScript中就是用一个变量名表示，变量名是大小写英文、数字、$和_的组合，且不能用数字开头。变量名也不能是JavaScript的关键字，如if、while等。申明一个变量用var语句，比如：

```js
var a; // 申明了变量a，此时a的值为undefined
var $b = 1; // 申明了变量$b，同时给$b赋值，此时$b的值为1
var s_007 = '007'; // s_007是一个字符串
var Answer = true; // Answer是一个布尔值true
var t = null; // t的值是null
```

在JavaScript中，使用等号=对变量进行赋值。可以把任意数据类型赋值给变量，同一个变量可以反复赋值，而且可以是不同类型的变量，但是要注意只能用var申明一次，例如：

```js
var a = 123; // a的值是整数123
a = 'ABC'; // a变为字符串
```

要显示变量的内容，可以用console.log(x)
```js
var x = 100;
console.log(x);
```

### 数据类型

javascript 的数据类型分两类，原始类型和对象类型。
原始类型包括数字、字符串和布尔。
javascript 还有两个特殊的原始值： null（空），undefined（声明一个变量但未赋值）。
对象是属性的集合，每个属性由键/值对组成（值可以是原始类型也可以是对象）

#### 数字
JavaScript不区分整数和浮点数，所有数字均用number表示：
```js
1   
2.01
0xff  //十六进制
0o1   // 八进制
1.2345e3 // 科学计数法
```

#### 字符串
字符串是以单引号'或双引号"括起来的任意文本，比如'abc'，"xyz"等等。

```js
var a='abc'
var b="abc"
var c=`a
b
c
`
```
把多个字符串加起来
```js
var name = '小明';
var age = 20;
var message = '你好, ' + name + ', 你今年' + age + '岁了!';
console.log(message);
```
如果有很多变量需要连接，用+号就比较麻烦。ES6新增了一种模板字符串，表示方法和上面的多行字符串一样，但是它会自动替换字符串中的变量：
```js
var name = '小明';
var age = 20;
var message = `你好, ${name}, 你今年${age}岁了!`;
console.log(message);
```

字符串常见的操作如下：
```js
var s = 'Hello, world!';
s.length; // 13
```

要获取字符串某个指定位置的字符，与python相同：
```js
var s = 'Hello, world!';

s[0]; // 'H'
s[6]; // ' '
s[7]; // 'w'
s[12]; // '!'
s[13]; // undefined 超出范围的索引不会报错，但一律返回undefined
```

需要特别注意的是，字符串是不可变的，如果对字符串的某个索引赋值，不会有任何错误(与python不同，python直接报错)，但是，也没有任何效果：
```js
var s = 'Test';
s[0] = 'X';
alert(s); // s仍然为'Test'
```

#### 布尔值
布尔值和布尔代数的表示完全一致，一个布尔值只有true、false两种值，要么是true，要么是false，可以直接用true、false表示布尔值，也可以通过布尔运算计算出来：
```js
true; // 这是一个true值
false; // 这是一个false值
2 > 1; // 这是一个true值
2 >= 3; // 这是一个false值
```

#### null和undefined

null值表示一个空对象指针，指示变量未指向任何对象。
```js
document.getElementById("container");
```


undefined表示值未定义。声明了一个变量，但未对其初始化时，这个变量的值就是undefined。
```js
var b;
```

### 对象
JavaScript的对象是属性的无序集合，每个属性都是一个键/值对。

JavaScript的对象用于描述现实世界中的某个对象。例如，为了描述“小明”这个淘气的小朋友，我们可以用若干键值对来描述他：

```js
var xiaoming = {
    name: '小明',
    birth: 1990,
    school: 'No.1 Middle School',
    height: 1.70,
    weight: 65,
    score: null
};
```
JavaScript用一个{...}表示一个对象，键值对以xxx: xxx形式申明，用,隔开。

上述对象申明了一个name属性，值是'小明'，birth属性，值是1990，以及其他一些属性。最后，把这个对象赋值给变量xiaoming后，就可以通过变量xiaoming来获取小明的属性了：

```js
xiaoming.name; // '小明'
xiaoming.birth; // 1990
```

访问属性是通过.操作符完成的，但这要求属性名必须是一个有效的变量名(字母、数字、$、_)。如果属性名包含特殊字符，就必须用''括起来：
```js
var xiaohong = {
    name: '小红',
    'middle-school': 'No.1 Middle School'
};
```

xiaohong的属性名middle-school不是一个有效的变量，就需要用''括起来。访问这个属性也无法使用.操作符，必须用['xxx']来访问：
```js
xiaohong['middle-school']; // 'No.1 Middle School'
xiaohong['name']; // '小红'
xiaohong.name; // '小红'
```

也可以用xiaohong['name']来访问xiaohong的name属性，不过xiaohong.name的写法更简洁。我们在编写JavaScript代码的时候，属性名尽量使用标准的变量名，这样就可以直接通过object.prop的形式访问一个属性了。

实际上JavaScript对象的所有属性都是字符串，不过属性对应的值可以是任意数据类型。
如果访问一个不存在的属性会返回什么呢？JavaScript规定，访问不存在的属性不报错，而是返回undefined：

```js
var xiaoming = {
    name: '小明'
};

console.log(xiaoming.name);
console.log(xiaoming.age); // undefined
```

如果我们要检测xiaoming是否拥有某一属性，可以用in操作符：
```js
var xiaoming = {
    name: '小明',
    birth: 1990,
    school: 'No.1 Middle School',
    height: 1.70,
    weight: 65,
    score: null
};
'name' in xiaoming; // true
'grade' in xiaoming; // false
```


### 数组
JavaScript的数组可以包含任意数据类型（与python列表类似），并通过索引来访问每个元素。

要取得Array的长度，直接访问length属性：
```js
var arr = [1, 2, 3.14, 'Hello', null, true];
arr.length; // 6
```

请注意，直接给数组的length赋一个新的值会导致Array大小的变化：
```js
var arr = [1, 2, 3];
arr.length; // 3
arr.length = 6;
arr; // arr变为[1, 2, 3, undefined, undefined, undefined]
arr.length = 2;
arr; // arr变为[1, 2]
```

数组可以通过索引把对应的元素修改为新的值，因此，对Array的索引进行赋值会直接修改这个Array：

```js
var arr = ['A', 'B', 'C'];
arr[1] = 99;
arr; // arr现在变为['A', 99, 'C']
```

请注意，如果通过索引赋值时，索引超过了范围，同样会引起Array大小的变化：
```js
var arr = [1, 2, 3];
arr[5] = 'x';
arr; // arr变为[1, 2, 3, undefined, undefined, 'x']
```

indexOf
与String类似，Array也可以通过indexOf()来搜索一个指定的元素的位置：

```js
var arr = [10, 20, '30', 'xyz'];
arr.indexOf(10); // 元素10的索引为0
arr.indexOf(20); // 元素20的索引为1
arr.indexOf(30); // 元素30没有找到，返回-1
arr.indexOf('30'); // 元素'30'的索引为2
```

slice
slice()就是对应String的substring()版本，它截取Array的部分元素，然后返回一个新的Array：
```js
var arr = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
arr.slice(0, 3); // 从索引0开始，到索引3结束，但不包括索引3: ['A', 'B', 'C']
arr.slice(3); // 从索引3开始到结束: ['D', 'E', 'F', 'G']
```

如果不给slice()传递任何参数，它就会从头到尾截取所有元素。利用这一点，我们可以很容易地复制一个数组:
```js
var arr = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
var aCopy = arr.slice();
aCopy; // ['A', 'B', 'C', 'D', 'E', 'F', 'G']
aCopy === arr; // false
```

push和pop
push()向Array的末尾添加若干元素，pop()则把Array的最后一个元素删除掉：
```js
var arr = [1, 2];
arr.push('A', 'B'); // 返回Array新的长度: 4
arr; // [1, 2, 'A', 'B']
arr.pop(); // pop()返回'B'
arr; // [1, 2, 'A']
arr.pop(); arr.pop(); arr.pop(); // 连续pop 3次
arr; // []
arr.pop(); // 空数组继续pop不会报错，而是返回undefined
arr; // []
```

sort
sort()可以对当前Array进行排序，它会直接修改当前Array的元素位置，直接调用时，按照默认顺序排序：
···js
var arr = ['B', 'C', 'A'];
arr.sort();
arr; // ['A', 'B', 'C']
···

join
join()方法是一个非常实用的方法，它把当前Array的每个元素都用指定的字符串连接起来，然后返回连接后的字符串：
```js
var arr = ['A', 'B', 'C', 1, 2, 3];
arr.join('-'); // 'A-B-C-1-2-3'
```

### 条件判断
JavaScript使用if () { ... } else { ... }来进行条件判断。例如，根据年龄显示不同内容，可以用if语句实现如下
```js
var age = 20;
if (age >= 18) { // 如果age >= 18为true，则执行if语句块
    alert('adult');
} else { // 否则执行else语句块
    alert('teenager');
}

```

其中else语句是可选的。如果语句块只包含一条语句，那么可以省略{}：
```js
var age = 20;
if (age >= 18)
    alert('adult');
else
    alert('teenager');
```

省略{}的危险之处在于，如果后来想添加一些语句，却忘了写{}，就改变了if...else...的语义，例如：
```js
var age = 20;
if (age >= 18)
    alert('adult');
else
    console.log('age < 18'); // 添加一行日志
    alert('teenager'); // <- 这行语句已经不在else的控制范围了
```

多行条件判断
如果还要更细致地判断条件，可以使用多个if...else...的组合：
```js
var age = 3;
if (age >= 18) {
    alert('adult');
} else if (age >= 6) {
    alert('teenager');
} else {
    alert('kid');
}
```

### 循环

#### for
JavaScript的循环有两种，一种是for循环，通过初始条件、结束条件和递增条件来循环执行语句块：
```js
var x = 0;
var i;
for (i=1; i<=10000; i++) {
    x = x + i;
}
x; // 50005000

```


让我们来分析一下for循环的控制条件：

i=1 这是初始条件，将变量i置为1；
i<=10000 这是判断条件，满足时就继续循环，不满足就退出循环；
i++ 这是每次循环后的递增条件，由于每次循环后变量i都会加1，因此它终将在若干次循环后不满足判断条件i<=10000而退出循环。


for循环最常用的地方是利用索引来遍历数组：
```js
var arr = ['Apple', 'Google', 'Microsoft'];
var i, x;
for (i=0; i<arr.length; i++) {
    x = arr[i];
    console.log(x);
}
```

continue 语句跳过后面语句，直接进入下一次循环
```js
for(i=1;i<=6;i++){
    if (i==2){
        continue
    }
    console.log(i)
}
```
#### while
for循环在已知循环的初始和结束条件时非常有用。而上述忽略了条件的for循环容易让人看不清循环的逻辑，此时用while循环更佳。

while循环只有一个判断条件，条件满足，就不断循环，条件不满足时则退出循环。比如我们要计算100以内所有奇数之和，可以用while循环实现：

```js
var x = 0;
var n = 99;
while (n > 0) {
    x = x + n;
    n = n - 2;
}
x; // 2500
```

在循环内部变量n不断自减，直到变为-1时，不再满足while条件，循环退出。


### 函数

定义函数
在JavaScript中，定义函数的方式如下：
```js
function abs(x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
}
```

上述abs()函数的定义如下：

+ function指出这是一个函数定义；
+ abs是函数的名称；
+ (x)括号内列出函数的参数，多个参数以,分隔；
+ { ... }之间的代码是函数体，可以包含若干语句，甚至可以没有任何语句。
请注意，函数体内部的语句在执行时，一旦执行到return时，函数就执行完毕，并将结果返回。因此，函数内部通过条件判断和循环可以实现非常复杂的逻辑。

如果没有return语句，函数执行完毕后也会返回结果，只是结果为undefined。

由于JavaScript的函数也是一个对象，上述定义的abs()函数实际上是一个函数对象，而函数名abs可以视为指向该函数的变量。

因此，第二种定义函数的方式如下：

```js
var abs = function (x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
};
```

在这种方式下，function (x) { ... }是一个匿名函数，它没有函数名。但是，这个匿名函数赋值给了变量abs，所以，通过变量abs就可以调用该函数。

上述两种定义完全等价，注意第二种方式按照完整语法需要在函数体末尾加一个;，表示赋值语句结束。

调用函数
调用函数时，按顺序传入参数即可：
```js
abs(10); // 返回10
abs(-9); // 返回9
```

由于JavaScript允许传入任意个参数而不影响调用，因此传入的参数比定义的参数多也没有问题，虽然函数内部并不需要这些参数：
```js
abs(10, 'blablabla'); // 返回10
abs(-9, 'haha', 'hehe', null); // 返回9
```

传入的参数比定义的少也没有问题：
```js
abs(); // 返回NaN
```

此时abs()函数的参数x将收x到undefined，计算结果为NaN。

要避免收到undefined，可以对参数进行检查：
```js
function abs(x) {
    if (typeof x !== 'number') {
        throw 'Not a number';
    }
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
}
```

arguments
JavaScript还有一个免费赠送的关键字arguments，它只在函数内部起作用，并且永远指向当前函数的调用者传入的所有参数。arguments类似Array但它不是一个Array：

```js
function foo(x) {
    console.log('x = ' + x); // 10
    for (var i=0; i<arguments.length; i++) {
        console.log('arg ' + i + ' = ' + arguments[i]); // 10, 20, 30
    }
}
foo(10, 20, 30);
```

### 方法

在一个对象中绑定函数，称为这个对象的方法。

在JavaScript中，对象的定义是这样的：
```js
var xiaoming = {
    name: '小明',
    birth: 1990
};
```

但是，如果我们给xiaoming绑定一个函数，就可以做更多的事情。比如，写个age()方法，返回xiaoming的年龄：
```js
var xiaoming = {
    name: '小明',
    birth: 1990,
    age: function () {
        var y = new Date().getFullYear();
        return y - this.birth;
    }
};

xiaoming.age; // function xiaoming.age()
xiaoming.age(); // 今年调用是29,明年调用就变成30了
```

绑定到对象上的函数称为方法，和普通函数也没啥区别，但是它在内部使用了一个this关键字

在一个方法内部，this是一个特殊变量，它始终指向当前对象，也就是xiaoming这个变量。所以，this.birth可以拿到xiaoming的birth属性。

```js
function getAge() {
    var y = new Date().getFullYear();
    return y - this.birth;
}

var xiaoming = {
    name: '小明',
    birth: 1990,
    age: getAge
};
xiaoming.age(); // 25, 正常结果

```

## 客户端js
浏览器里的javascript，如何操作html，css，如何发出ajax请求

### 操作dom

[DOM](https://www.runoob.com/htmldom/htmldom-tutorial.html)
由于HTML文档被浏览器解析后就是一棵DOM树，要改变HTML的结构，就需要通过JavaScript来操作DOM。
![img](./Chapter-07/pics/pic_htmltree.gif)

始终记住DOM是一个树形结构。操作一个DOM节点实际上就是这么几个操作：

+ 更新：更新该DOM节点的内容，相当于更新了该DOM节点表示的HTML的内容；

+ 遍历：遍历该DOM节点下的子节点，以便进行进一步操作；

+ 添加：在该DOM节点下新增一个子节点，相当于动态增加了一个HTML节点；

+ 删除：将该节点从HTML中删除，相当于删掉了该DOM节点的内容以及它包含的所有子节点。

在操作一个DOM节点前，我们需要通过各种方式先拿到这个DOM节点。最常用的方法是document.getElementById()和document.getElementsByTagName()，以及CSS选择器document.getElementsByClassName()。

由于ID在HTML文档中是唯一的，所以document.getElementById()可以直接定位唯一的一个DOM节点。document.getElementsByTagName()和document.getElementsByClassName()总是返回一组DOM节点。要精确地选择DOM，可以先定位父节点，再从父节点开始选择，以缩小范围。

例如:
```js
<style>
.red {
    color: red;
}
</style>

<div id="test">

<table id="test-table" border=10>
  <tr class="red">
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table>
</div>



// 返回ID为'test'的节点：
var test = document.getElementById('test');

// 先定位ID为'test-table'的节点，再返回其内部所有tr节点：
var trs = document.getElementById('test-table').getElementsByTagName('tr');

// 先定位ID为'test-div'的节点，再返回其内部所有class包含red的节点：
var reds = document.getElementById('test').getElementsByClassName('red');

// 获取节点test下的所有直属子节点:
var cs = test.children;

// 获取节点test下第一个、最后一个子节点：
var first = test.firstElementChild;
var last = test.lastElementChild;
```

第二种方法是使用`querySelector()`和`querySelectorAll()`，需要了解selector语法，然后使用条件来获取节点，更加方便：
```js
// 通过querySelector获取ID为test的节点：
var q1 = document.querySelector('#test');

// 通过querySelectorAll获取q1节点内的符合条件的所有节点：
var ps = q1.querySelectorAll('tr.red > th');
```

### 更新DOM
拿到一个DOM节点后，我们可以对它进行更新。

可以直接修改节点的文本，方法有两种：

一种是修改innerHTML属性，这个方式非常强大，不但可以修改一个DOM节点的文本内容，还可以直接通过HTML片段修改DOM节点内部的子树：
```js
<p id="p-id">innerhtml</p>

<script>
var p = document.getElementById('p-id');
// 设置文本为abc:
p.innerHTML = 'ABC'; // <p id="p-id">ABC</p>
// 设置HTML:
p.innerHTML = 'ABC <span style="color:red">RED</span> XYZ';

</script>
```

第二种是修改innerText，这样可以设置文本，防止出现解析html元素：
```js
<p id="p-id">innerhtml</p>

<script>
// 获取<p id="p-id">...</p>
var p = document.getElementById('p-id');
// 设置文本:
p.innerText = '<p>dd</p>';
// HTML被自动编码，无法设置一个子节点:

</script>
```

练习
有如下的HTML结构：
```html
<!-- HTML结构 -->
<div id="test-div">
  <p id="test-js">javascript</p>
  <p>Java</p>
</div>
```

获取`<p>javascript</p>`节点,修改文本为JavaScript test

答案
```html
<!-- HTML结构 -->
<div id="test-div">
  <p id="test-js">javascript</p>
  <p>Java</p>
</div>

<script>

var p = document.getElementById('test-js');

p.innerText = 'JavaScript test';


</script>
```

### 插入DOM 
当我们获得了某个DOM节点，想在这个DOM节点内插入新的DOM，应该如何做？

如果这个DOM节点是空的，例如，`<div></div>`，那么，直接使用`innerHTML = '<span>child</span>'`就可以修改DOM节点的内容，相当于“插入”了新的DOM节点。

如果这个DOM节点不是空的，那就不能这么做，因为innerHTML会直接替换掉原来的所有子节点。

有两个办法可以插入新的节点。一个是使用appendChild，把一个子节点添加到父节点的最后一个子节点。例如：
```html
<!-- HTML结构 -->
<p id="js">JavaScript</p>
<div id="list">
    <p id="java">Java</p>
    <p id="python">Python</p>
    <p id="scheme">Scheme</p>
</div>
```

把`<p id="js">JavaScript</p>`添加到`<div id="list">`的最后一项：
```
var js = document.getElementById('js');
var list = document.getElementById('list');
list.appendChild(js);
```

现在，HTML结构变成了这样：
```html
<!-- HTML结构 -->
<div id="list">
    <p id="java">Java</p>
    <p id="python">Python</p>
    <p id="scheme">Scheme</p>
    <p id="js">JavaScript</p>
</div>
```

因为我们插入的js节点已经存在于当前的文档树，因此这个节点首先会从原先的位置删除，再插入到新的位置。

更多的时候我们会从零创建一个新的节点，然后插入到指定位置：
```js
var
    list = document.getElementById('list'),
    haskell = document.createElement('p');
haskell.id = 'haskell';
haskell.innerText = 'Haskell';
list.appendChild(haskell);
```
document.createElement('p')创建一个p节点
这样我们就动态添加了一个新的节点：
```html
<!-- HTML结构 -->
<div id="list">
    <p id="java">Java</p>
    <p id="python">Python</p>
    <p id="scheme">Scheme</p>
    <p id="haskell">Haskell</p>
</div>
```
动态创建一个节点然后添加到DOM树中，可以实现很多功能。举个例子，下面的代码动态创建了一个`<style>`节点，然后把它添加到`<head>`节点的末尾，这样就动态地给文档添加了新的CSS定义：
```js
var d = document.createElement('style');
d.setAttribute('type', 'text/css');
d.innerHTML = 'p { color: red }';
document.getElementsByTagName('head')[0].appendChild(d);
```

### 删除DOM
删除一个DOM节点就比插入要容易得多。

要删除一个节点，首先要获得该节点本身以及它的父节点，然后，调用父节点的removeChild把自己删掉：
```html
<!-- HTML结构 -->
<div id="list">
    <p id="java">Java</p>
    <p id="python">Python</p>
    <p id="scheme">Scheme</p>
</div>

<script>

// 拿到待删除节点:
var self = document.getElementById('scheme');
// 拿到父节点:
var parent = self.parentElement;
// 删除:
var removed = parent.removeChild(self);

</script>
```

### 操作表单
用JavaScript操作表单和操作DOM是类似的，因为表单本身也是DOM树。

不过表单的输入框、下拉框等可以接收用户输入，所以用JavaScript来操作表单，可以获得用户输入的内容，或者对一个输入框设置新的内容。

HTML表单的输入控件主要有以下几种：
+ 文本框，对应的`<input type="text">`，用于输入文本；
+ 口令框，对应的`<input type="password">`，用于输入口令；
+ 单选框，对应的`<input type="radio">`，用于选择一项；
+ 复选框，对应的`<input type="checkbox">`，用于选择多项；
+ 下拉框，对应的`<select>`，用于选择一项；

隐藏文本，对应的`<input type="hidden">`，用户不可见，但表单提交时会把隐藏文本发送到服务器。

#### 获取值
```html
<!-- HTML结构 -->
<form>
<input type="text" id="user" value="jiam">
</form>

<script>
var input = document.getElementById('user');
console.log(input.value);
</script>
```

这种方式可以应用于text、password、hidden以及select。但是，对于单选框和复选框，value属性返回的永远是HTML预设的值，而我们需要获得的实际是用户是否“勾上了”选项，所以应该用checked判断：
```html
<!-- HTML结构 -->
<form>
<input type="text" id="user" value="jiam">
<label>monday</label>
<input type="radio" name="weekday" id="monday" value="1"> 
<label>tuesday</label>
<input type="radio" name="weekday" id="tuesday" value="2">
</form>

<script>
var mon = document.getElementById('monday');
var tue = document.getElementById('tuesday');
mon.value; // '1'
tue.value; // '2'
mon.checked; // true或者false
tue.checked; // true或者false


</script>
```
#### 设置值
设置值和获取值类似，对于text、password、hidden以及select，直接设置value就可以：
```js

var input = document.getElementById('user');
input.value = 'jiaminqiang'; // 文本框的内容已更新
tue.checked = true

```
#### 提交表单
```html
<!-- HTML -->
<form id="test-form">
    <input type="text" name="test">
    <button type="button" onclick="doSubmitForm()">Submit</button>
</form>

<script>
function doSubmitForm() {
    var form = document.getElementById('test-form');
    // 可以在此修改form的input...
    // 提交form:
    form.submit();
}
</script>
```


### 修改css
修改CSS也是经常需要的操作。DOM节点的style属性对应所有的CSS，可以直接获取或设置。因为CSS允许font-size这样的名称，但它并非JavaScript有效的属性名，所以需要在JavaScript中改写为驼峰式命名fontSize：

```html
<!-- HTML -->
<p id="p-id">修改css</p>

<script>

var p = document.getElementById('p-id');
// 设置CSS:
p.style.color = '#ff0000';
p.style.fontSize = '20px';
p.style.paddingTop = '2em';
</script>
```

### 事件
因为JavaScript在浏览器中以单线程模式运行，页面加载后，一旦页面上所有的JavaScript代码被执行完后，就只能依赖触发事件来执行JavaScript代码。

浏览器在接收到用户的鼠标，会自动在对应的DOM节点上触发相应的事件。如果该节点已经绑定了对应的JavaScript处理函数，该函数就会自动调用。

常见的HTML事件
下面是一些常见的HTML事件的列表:
```
onchange	HTML 元素改变
onclick	用户点击 HTML 元素
onmouseover	用户在一个HTML元素上移动鼠标
onmouseout	用户从一个HTML元素上移开鼠标
onkeydown	用户按下键盘按键
onload	浏览器已完成页面的加载
```

### ajax
AJAX是Asynchronous JavaScript and XML的缩写，意思就是用JavaScript执行异步网络请求。

如果仔细观察一个Form的提交，你就会发现，一旦用户点击“Submit”按钮，表单开始提交，浏览器就会刷新页面，然后在新页面里告诉你操作是成功了还是失败了。如果不幸由于网络太慢或者其他原因，就会得到一个404页面。

这就是Web的运作原理：一次HTTP请求对应一个页面。

如果要让用户留在当前页面中，同时发出新的HTTP请求，就必须用JavaScript发送这个新请求，接收到数据后，再用JavaScript更新页面，这样一来，用户就感觉自己仍然停留在当前页面，但是数据却可以不断地更新。

在浏览器上写AJAX主要依靠XMLHttpRequest对象：

```js
var request = new XMLHttpRequest();
request.open("GET", "/")
request.send()
```

发一个post请求
```javascript
function encodeFormData(o){
   var s="";
    for (var item in o) {
       s = s + item +"=" + o[item] +"&"     
}
    return  s.substring(0,s.length-1)
}

function callback(request) {
     console.log(request.status)
}

function postData(url, data, callback) {
    var request = new XMLHttpRequest();
    request.open("post", url);
    request.onreadystatechange = function(){
        if ((request.readyState === 4) && callback)
            callback(request);
    };
    request.setRequestHeader("Content-Type",
        "application/x-www-form-urlencode");
    request.send(encodeFormData(data));
}

var data = {name:"jia", age:"20"}
var url = 'http://httpbin.org/post'
postData(url, data ,callback)
```

发送一个带参数的get请求
```javascript
function encodeFormData(o){
   var s="";
    for (var item in o) {
       s = s + item +"=" + o[item] +"&"     
    }
    return  s.substring(0,s.length-1)
}

function callback(request) {
     console.log(request.status)
}

function getData(url, data, callback) {
    var request = new XMLHttpRequest();
    request.open("GET", url + "?" + encodeFormData(data));
    request.onreadystatechange = function() {
        if ((request.readyState === 4) && callback)
            callback(request);
    }
    request.send()
}

var data = {name:"jia", age:"20"}
var url = 'http://httpbin.org/get'
getData(url, data, callback)
```
成功处理，失败处理 
```javascript
function success(text) {
    console.log(text)
}

function fail(code) {
   console.log(code)
}

var request = new XMLHttpRequest(); // 新建XMLHttpRequest对象

request.onreadystatechange = function () { // 状态发生变化时，函数被回调
    if (request.readyState === 4) { // 成功完成
        // 判断响应结果:
        if (request.status === 200) {
            // 成功，通过responseText拿到响应的文本:
            return success(request.responseText);
        } else {
            // 失败，根据响应码判断失败原因:
            return fail(request.status);
        }
    } else {
        // HTTP请求还在继续...
    }
}

// 发送请求:
request.open('GET', 'http://httpbin.org/get');
request.send();
```

## jquery

使用jQuery只需要在页面的`<head>`引入jQuery文件即可：
```html
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
</head>
<body>
</body>
</html>

<script>
console.log('jQuery版本：' + $.fn.jquery);
</script>
```

### $符号


`$`是著名的jQuery符号。实际上，jQuery把所有功能全部封装在一个全局变量jQuery中，而$也是一个合法的变量名，它是变量jQuery的别名：
```javascript
window.jQuery; // jQuery(selector, context)
window.$; // jQuery(selector, context)
$ === jQuery; // true
typeof($); // 'function'
```

$本质上就是一个函数，但是函数也是对象，于是$除了可以直接调用外，也可以有很多其他属性。

注意，你看到的$函数名可能不是jQuery(selector, context)，
```javascript
$ = 1
$ === jQuery;
```
### 定位元素

如果某个DOM节点有id属性，利用jQuery查找如下：

```html
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
</head>
<body>
<div id="abc">
<p> jquery id </p>
<p> jquery id </p>
</div>
</body>
</html>

<script>
// 查找<div id="abc">:
var div = $('#abc');
div[0]
</script>
```

注意，#abc以#开头。返回的对象是jQuery对象。
什么是jQuery对象？jQuery对象类似数组，它的每个元素都是一个引用了DOM节点的对象。

以上面的查找为例，如果id为abc的<div>存在，返回的jQuery对象如下：
```
m.fn.init [div#abc, context: document, selector: "#abc"]
```
如果id为abc的<div>不存在，返回的jQuery对象如下：
`m.fn.init {context: document, selector: "#d"}`

按tag查找只需要写上tag名称就可以了：
```js
var ps = $('p'); // 返回所有<p>节点
ps.length; // 数一数页面有多少个<p>节点
ps[0]
```

按class查找注意在class名称前加一个.：
html
```html
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
    <style>
    .red {
          color: red
     }
    </style>
</head>
<body>
<div id="abc">
<p class='red'> jquery id </p>
<p> jquery id </p>
</div>
</body>
</html>
```
script
```js
var a = $('.red'); // 所有节点包含`class="red"`都将返回
a[0]
```

一个DOM节点除了id和class外还可以有很多属性
html
```html
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
    <style>
    .red {
          color: red
     }
    </style>
</head>
<body>
<form>
<input type="text" id="user" name="user" value="jiam">
<label>monday</label>
<input type="radio" name="weekday" id="monday" value="1"> 
<label>tuesday</label>
<input type="radio" name="weekday" id="tuesday" value="2">
</form>
</body>
</html>
```
javascript
```js
var user = $('[name=user]'); 
user[0];
var password = $('[type=password]'); 
password[0];
```

### 修改CSS
```html
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
    <style>
    .lang {
          color: red
     }
    .lang-javascript {
          color:  green
     }
    .lang-python{
           color: yellow
     }
    .lang-lua{
           color:  blue
     }
    </style>
</head>
<body>
<ul id="test-css">
    <li class="lang"><span>JavaScript</span></li>
    <li class="lang"><span>Java</span></li>
    <li class="lang"><span>Python</span></li>
    <li class="lang"><span>Swift</span></li>
    <li class="lang"><span>Scheme</span></li>
</ul>
</body>
</html>
```

要高亮显示动态语言，调用jQuery对象的css('name', 'value')方法，我们用一行语句实现：
```js
$('#test-css li.lang>span').css('background-color', '#ffd351').css('color', 'green');
```
注意，jQuery对象的所有方法都返回一个jQuery对象（可能是新的也可能是自身），这样我们可以进行链式调用，非常方便。

jQuery对象的css()方法可以这么用：
```js
var li = $('li');
li.css('color'); // '#000033', 获取CSS属性
```

如果要修改class属性，可以用jQuery提供的下列方法：
```js
var div = $('#test-div');
div.hasClass('highlight'); // false， class是否包含highlight
div.addClass('highlight'); // 添加highlight这个class
div.removeClass('highlight'); // 删除highlight这个class
```

### 操作dom
#### 修改Text和HTML
jQuery对象的text()和html()方法分别获取节点的文本和原始HTML文本，例如，如下的HTML结构：
```html
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
 
</head>
<body>


<div id="test-div" name="test">
<ul id="test-ul">
    <li class="js">JavaScript</li>
    <li name="book">Java &amp; JavaScript</li>
</ul>
</div>
</body>
</html>


```

分别获取文本和HTML：
```js
$('#test-ul li[name=book]').text(); // 'Java & JavaScript'
$('#test-ul li[name=book]').html(); // 'Java &amp; JavaScript'
```

设置
```js
$('#test-ul li').text('JS'); // 是不是两个节点都变成了JS？
```

#### 显示和隐藏DOM
要隐藏一个DOM，我们可以设置CSS的display属性为none，利用css()方法就可以实现。不过，要显示这个DOM就需要恢复原有的display属性，这就得先记下来原有的display属性到底是block还是inline还是别的值。

考虑到显示和隐藏DOM元素使用非常普遍，jQuery直接提供show()和hide()方法，我们不用关心它是如何修改display属性的，总之它能正常工作：

```js
var li = $('li');
li.hide(); // 隐藏
li.show(); // 显示
```

注意，隐藏DOM节点并未改变DOM树的结构，它只影响DOM节点的显示。这和删除DOM节点是不同的。

获取DOM信息
利用jQuery对象的若干方法，我们直接可以获取DOM的高宽等信息，而无需针对不同浏览器编写特定代码
```js
// 浏览器可视窗口大小:
$(window).width(); // 800
$(window).height(); // 600

// HTML文档大小:
$(document).width(); // 800
$(document).height(); // 3500

// 某个div的大小:
var div = $('#test-div');
div.width(); // 600
div.height(); // 300
div.width(400); // 设置CSS属性 width: 400px，是否生效要看CSS是否有效
div.height('200px'); // 设置CSS属性 height: 200px，是否生效要看CSS是否有效
```

attr()和removeAttr()方法用于操作DOM节点的属性：
···
// <div id="test-div" name="Test" >...</div>
var div = $('#test-div');
div.attr('data'); // undefined, 属性不存在
div.attr('name'); // 'Test'
div.attr('name', 'Hello'); // div的name属性变为'Hello'
div.removeAttr('name'); // 删除name属性
div.attr('name'); // undefined
···

### 操作表单
对于表单元素，jQuery对象统一提供val()方法获取和设置对应的value属性：
```js
/*
    <input id="test-input" name="email" value="">
    <select id="test-select" name="city">
        <option value="BJ" selected>Beijing</option>
        <option value="SH">Shanghai</option>
        <option value="SZ">Shenzhen</option>
    </select>
    <textarea id="test-textarea">Hello</textarea>
*/
var
    input = $('#test-input'),
    select = $('#test-select'),
    textarea = $('#test-textarea');

input.val(); // 'test'
input.val('abc@example.com'); // 文本框的内容已变为abc@example.com

select.val(); // 'BJ'
select.val('SH'); // 选择框已变为Shanghai

textarea.val(); // 'Hello'
textarea.val('Hi'); // 文本区域已更新为'Hi'
```

可见，一个val()就统一了各种输入框的取值和赋值的问题。

### 添加节点
要添加新的DOM节点，除了通过jQuery的html()这种暴力方法外，还可以用append()方法，例如：
```html
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
 
</head>
<body>


 <div id="test-div">
    <ul>
        <li><span>JavaScript</span></li>
        <li><span>Python</span></li>
        <li id="swift"><span>Swift</span></li>
    </ul>
</div>
</body>
</html>

```

如何向列表新增一个语言？首先要拿到`<ul>`节点：

`var ul = $('#test-div>ul');`

然后，调用append()传入HTML片段：

`ul.append('<li><span>Haskell</span></li>');`

### 删除节点
要删除DOM节点，拿到jQuery对象后直接调用remove()方法就可以了。如果jQuery对象包含若干DOM节点，实际上可以一次删除多个DOM节点：
```js
var li = $('#test-div>ul>li');
li.remove(); // 所有<li>全被删除
```

### 事件
jquery 绑定事件
举个例子，假设要在用户点击了超链接时弹出提示框，我们用jQuery这样绑定一个click事件：

```html
<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
 
</head>
<body>


 <a id="test-link" href="#0">点我试试</a>
</body>
</html>


```
javascript
```js
// 获取超链接的jQuery对象:
var a = $('#test-link');
a.on('click', function () {
    alert('Hello!');
});
```

on方法用来绑定一个事件，我们需要传入事件名称和对应的处理函数。

另一种更简化的写法是直接调用click()方法：
```js
a.click(function () {
    alert('Hello!');
});
```

### AJAX函数
ajax
jQuery在全局对象jQuery（也就是$）绑定了ajax()函数，可以处理AJAX请求。ajax(url, settings)函数需要接收一个URL和一个可选的settings对象，常用的选项如下：

+ url： 请求的url

+ type：发送的Method，缺省为'GET'，可指定为'POST'、'PUT'等；

+ contentType：发送POST请求的格式，默认值为'application/x-www-form-urlencoded; charset=UTF-8'，也可以指定为text/plain、application/json；

+ data：发送的数据，可以是字符串、数组或object。如果是GET请求，data将被转换成query附加到URL上，如果是POST请求，根据contentType把data序列化成合适的格式；




发送一个get请求
```js
var jqxhr = $.ajax('/');
// 请求已经发送了
```

发送一个json请求,并展示数据
```html

<html>
<head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
</head>
<body>
<h2>返回数据</h2>
<p></p>
</body>
</html>
```

```js
 content = {
     name: "jia",
     age: 18
 }
 $.ajax({
            type: 'POST',
            url: 'https://httpbin.org/post',
            data: JSON.stringify(content),
            success: function(data){
                console.log(data)
                $("p").text(data.data)
             } ,
            contentType: 'application/json'
        });
```

对常用的AJAX操作，jQuery提供了一些辅助方法。由于GET请求最常见，所以jQuery提供了get()方法，可以这么写：
```js
var jqxhr = $.get('/path/to/resource', {
    name: 'Bob Lee',
    check: 1
});
```

第二个参数如果是object，jQuery自动把它变成query string然后加到URL后面，实际的URL是：

/path/to/resource?name=Bob%20Lee&check=1
这样我们就不用关心如何用URL编码并构造一个query string了。

post
post()和get()类似，但是传入的第二个参数默认被序列化为application/x-www-form-urlencoded：
```js
var jqxhr = $.post('/path/to/resource', {
    name: 'Bob Lee',
    check: 1
});
```
实际构造的数据name=Bob%20Lee&check=1作为POST的body被发送。


## 作业
1. 有如下html
```html
<div id="test-div">
  <p id="test-js">javascript</p>
  <p>Java</p>
</div>
```
+ 获取`<p>javascript</p>`
+ 修改文本为JavaScript
+ 修改CSS为: color: #ff0000, font-weight: bold

注： 使用javascript 和jquery实现

2. 有如下html
```html
<ul id="test-list">
    <li>JavaScript</li>
    <li>Swift</li>
    <li>HTML</li>
    <li>ANSI C</li>
    <li>CSS</li>
    <li>DirectX</li>
</ul>
```
+ 把与Web开发技术不相关的节点删掉
注： 使用javascript和jquery实现

3. 有如下html
```html
<div class="test-selector">
    <ul class="test-lang">
        <li class="lang-javascript">JavaScript</li>
        <li class="lang-python">Python</li>
        <li class="lang-lua">Lua</li>
    </ul>
    <ol class="test-lang">
        <li class="lang-swift">Swift</li>
        <li class="lang-java">Java</li>
        <li class="lang-c">C</li>
    </ol>
</div>
```

分别选择所有语言，所有动态语言，所有静态语言
注：  使用javascript和jquery实现

4. 有如下html
```html
<form id="test-form" action="#0" onsubmit="return false;">
    <p><label>Name: <input name="name"></label></p>
    <p><label>Email: <input name="email"></label></p>
    <p><label>Password: <input name="password" type="password"></label></p>
    <p>Gender: <label><input name="gender" type="radio" value="m" checked> Male</label> <label><input name="gender" type="radio" value="f"> Female</label></p>
    <p><label>City: <select name="city">
    	<option value="BJ" selected>Beijing</option>
    	<option value="SH">Shanghai</option>
    	<option value="CD">Chengdu</option>
    	<option value="XM">Xiamen</option>
    </select></label></p>
    <p><button type="submit">Submit</button></p>
</form>
```

输入值后，用jQuery获取表单的JSON字符串，key和value分别对应每个输入的name和相应的value，例如：{"name":"Michael","email":...}

5. 有如下html
```html
<form id="test-register" action="#" target="_blank" onsubmit="checkRegisterForm()">
    <p id="test-error" style="color:red"></p>
    <p>
        用户名: <input type="text" id="username" name="username">
    </p>
    <p>
        口令: <input type="password" id="password" name="password">
    </p>
    <p>
        重复口令: <input type="password" id="password-2">
    </p>
    <p>
        <button type="submit">提交</button> <button type="reset">重置</button>
    </p>
</form>
```
利用JavaScript检查用户注册信息是否正确，在以下情况不满足时报错并阻止提交表单：

+ 用户名必须是3-10位英文字母或数字；

+ 口令必须是6-20位；

+ 两次输入口令必须一致。

提示: 编写checkRegisterForm() 函数, 当函数返回值为ture 是表单提交，返回值为false表单不提交
检查失败时调用alert() 弹窗 并返回false

6. 有如下html：
```html
<!-- HTML结构 -->
<form id="test-form" action="test">
    <legend>请选择想要学习的编程语言：</legend>
    <fieldset>
        <p><label class="selectAll"><input type="checkbox"> <span class="selectAll">全选</span><span class="deselectAll"><input type="checkbox">全不选</span></label> 
        <p><label><input type="checkbox" name="lang" value="javascript"> JavaScript</label></p>
        <p><label><input type="checkbox" name="lang" value="python"> Python</label></p>
        <p><label><input type="checkbox" name="lang" value="ruby"> Ruby</label></p>
        <p><label><input type="checkbox" name="lang" value="haskell"> Haskell</label></p>
        <p><label><input type="checkbox" name="lang" value="scheme"> Scheme</label></p>
		<p><button type="submit">Submit</button></p>
    </fieldset>
</form>
```

1. 当用户勾上“全选”时，自动选中所有语言，并把“全选”变成“全不选”；

2. 当用户去掉“全不选”时，自动不选中所有语言；
