# Generated by Django 2.2.2 on 2021-07-10 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('httpapitest', '0003_testcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('report_name', models.CharField(max_length=40)),
                ('start_at', models.CharField(max_length=40, null=True)),
                ('status', models.BooleanField()),
                ('testsRun', models.IntegerField()),
                ('successes', models.IntegerField()),
                ('reports', models.TextField()),
            ],
            options={
                'verbose_name': '测试报告',
                'db_table': 'TestReports',
            },
        ),
    ]
