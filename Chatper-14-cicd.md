# CICD

## 线上环境部署

### 操作系统
centos 7

### 更换默认的yum源为阿里云
centos7
```
cd /etc/yum.repos.d/
rm -f ./*.repo
curl http://mirrors.aliyun.com/repo/Centos-7.repo -o /etc/yum.repos.d/CentOS-Base.repo
yum clean all
```


cetos6
```
cd /etc/yum.repos.d/
rm -f ./*.repo
curl http://mirrors.aliyun.com/repo/Centos-7.repo -o /etc/yum.repos.d/CentOS-Base.repo
yum clean all
```

### 部署代码
将代码传送到linux环境下的

安装一个ssh 工具用来远程登录linux

在linux中安装lrzsz `yum install lrzsz`

或者使用scp


执行rz 命令上传代码
### 安装redis
 ```
yum install epel-release
yum install redis
systemctl start redis

```

### 安装mysql
centos7
```
yum install mariadb mariadb-devel mariadb-server
#启动mysql-server
systemctl start mariadb
```
centos6
```
yum install mysql
yum install mysql-devel
# 启动
/etc/init.d/mysqld start
```

### anacoda 
一个python的发行版可快速在linux系统中配置python环境
https://repo.anaconda.com/archive/

下周anaconda linux版
`wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh`

安装anacod
```
sh ./Anaconda3-2019.07-Linux-x86_64.sh

Welcome to Anaconda3 2019.07

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue

>>>

输入回车

Do you accept the license terms? [yes|no]

输入yes
Anaconda3 will now be installed into this location:
/root/anaconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/root/anaconda3] >>>

输入/opt/anaconda3
回车

[/root/anaconda3] >>> /opt/anaconda3
PREFIX=/opt/anaconda3
Unpacking payload ...

installation finished.
Do you wish the installer to initialize Anaconda3
by running conda init? [yes|no]
[no] >>> no

```

### 配置虚拟环境

```
cd /opt/anaconda3/bin

./pip install virtualenv -i https://pypi.douban.com/simple/

cd /opt
/opt/anaconda3/bin/virtualenv env


source env/bin/activate
(env) [root@python-dev opt]#
```
### 从git上clone 项目
`yum install git`
`git clone https://github.com/jiam/hat.git`

### 查看项目依赖模块版本
`pip freeze`

新建requirements.txt文件
```
cat << EOF>requirements.txt
Django==2.2.2
celery==4.3.0
django-celery-beat==1.5.0
mysqlclient==1.4.2.post1
PyYAML==5.1
HttpRunner==2.2.2
gunicorn
redis
EOF
```
### 安装依赖模块
```
# 安装gcc
yum install gcc
mysqlclient 安装时需要gcc进行编译
# 在env环境下进入代码目录
cd /opt/hat
# 安装依赖模块
(env) [root@python-dev autotest]# pip install -r requirements.txt -i https://pypi.douban.com/simple/  

```
### 初始化数据库
```
# 连接数据库
mysql -uroot -p
# 创建数据库
create database hat /*!40100 DEFAULT CHARACTER SET utf8 */;

# 授权
grant all on hat.* to hatuser@`%` identified by 'hat2019'
grant all on hat.* to hatuser@`localhost` identified by 'hat2019'
# 退出数据库
quit
```

初始化书库表
`python manage.py makemigrations`
`python manage.py  migrate`

### 启动django应用

```
(env) [root@python-dev hat]# nohup gunicorn hat.wsgi >logs/gunicorn.log 2>&1 &
[1] 14207
(env) [root@python-dev hat]# tail gunicorn.log
nohup: ignoring input
[2018-09-08 11:09:45 +0000] [14207] [INFO] Starting gunicorn 19.9.0
[2018-09-08 11:09:45 +0000] [14207] [INFO] Listening at: http://127.0.0.1:8000 (14207)
[2018-09-08 11:09:45 +0000] [14207] [INFO] Using worker: sync
[2018-09-08 11:09:45 +0000] [14210] [INFO] Booting worker with pid: 14210
```

### 启动celery
```
nohup celery -A  hat  worker --loglevel=info >logs/celery.log 2>&1 &
nohup celery -A  hat  beat  --loglevel=info >logs/celery_beat.log 2>&1 &
```

### 启动nginx前提
关闭iptables
```
# centos7
systemctl disable firewalld
systemctl stop firewalld
# centos6
/etc/init.d/iptables stop

```
关闭selinux

`setenforce 0`
`sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config`

### 安装nginx




# 安装命令

```
rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
yum install nginx
systemctl start nginx
```

### 配置nginx
cat /etc/nginx/conf.d/default.conf

```
cat << EOF>/etc/nginx/conf.d/default.conf
server {
    listen       80;
    server_name  localhost;

    charset utf-8;
    access_log  /var/log/nginx/access.log  main;

    location / {
        proxy_pass http://localhost:8000;
    }

    location /static {
       alias  /opt/hat/static;
    }


    error_page  404              /404.html;

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
EOF
```


### reload
`nginx -s reload`

## docker 部署

### 安装docker
```
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install docker-ce docker-ce-cli containerd.io
```

### 配置docker 

```
mkdir /etc/docker
cat << EOF> /etc/docker/daemon.json
{
  "insecure-registries" : ["127.0.0.1:5000", "192.168.10.3:5000", "120.132.114.214:5000"],
  "registry-mirrors": [ "https://docker.mirrors.ustc.edu.cn" ],
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

```

### 启动docker
`systemctl start docker`

### 设置开启启动
`systemctl enable docker`


### 下载python3.7 镜像
`docker pull python:3.7`

### 运行python3.7
`docker run --rm -it  python:3.7  /bin/bash`

### 制作docker镜像

编写Dockerfile
```
cat << EOF>Dockerfile
FROM python:3.7


COPY sources.list  /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/hat
COPY requirements.txt ./

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/
COPY . .
COPY default  /etc/nginx/sites-enabled
CMD sh start.sh
EOF

cat << EOF>sources.list
deb http://mirrors.aliyun.com/debian/ stretch main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ stretch main non-free contrib
deb http://mirrors.aliyun.com/debian-security stretch/updates main
deb-src http://mirrors.aliyun.com/debian-security stretch/updates main
deb http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib
deb http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib

EOF

cat << EOF>start.sh
nohup gunicorn hat.wsgi >logs/gunicorn.log 2>&1 &
nohup celery -A  hat  worker --loglevel=info >logs/celery.log 2>&1 &
nohup celery -A  hat  beat  --loglevel=info >logs/celery_beat.log 2>&1 &
nginx -g 'daemon off;'
EOF

cat << EOF> default
server {
    listen       80 default_server;
    server_name  _;

    charset utf-8;
    access_log  /var/log/nginx/access.log;

    location / {
        proxy_pass http://localhost:8000;
    }

    location /static {
       alias  /opt/hat/static;
    }


    error_page  404              /404.html;

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
EOF
```

生成镜像命令
`docker build . -t hat:1.0`

运行镜像
systemctl stop nginx
`docker run -d --network=host  --name hat hat:1.0`


### mysql创建用户并授权

`grant all on hat.* to 'hatuser'@'%' identified by "hat2019";`

### 查看mysql当前用户
`select user,password,host from mysql.user;`

### 修改hat/settings.py


### mysql备份

`mysqldump -uroot -p hat >hat.sql`

### 导出表结构
`mysqldump -d -u root -p hat >hat.sql`

### 导出数据

`mysqldump     -t -u root -p hat >hat.sql`

### 导入数据

`mysql -uroot -p hat<hat.sql`


在mysql cli中执行
`source hat.sql`



### docker registry

docker 镜像的仓库
```
docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  -v /mnt/registry:/var/lib/registry \
  registry:2
```
### 向registry push image

```
docker tag hat:1.0 192.168.1.5:5000/hat:1.0
docker push 192.168.1.5:5000/hat:1.0
```

### 从仓库拉镜像
```
docker pull 192.168.1.5:5000/hat:1.0
```

### mysql 容器

https://hub.docker.com/_/mysql



