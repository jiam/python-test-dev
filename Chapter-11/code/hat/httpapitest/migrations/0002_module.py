# Generated by Django 2.2.2 on 2021-07-02 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('httpapitest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('module_name', models.CharField(max_length=50, verbose_name='模块名称')),
                ('test_user', models.CharField(max_length=50, verbose_name='测试负责人')),
                ('simple_desc', models.CharField(max_length=100, null=True, verbose_name='简要描述')),
                ('other_desc', models.CharField(max_length=100, null=True, verbose_name='其他信息')),
                ('belong_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='httpapitest.Project')),
            ],
            options={
                'verbose_name': '模块信息',
                'db_table': 'Module',
            },
        ),
    ]