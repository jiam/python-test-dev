from django.db import models
from django.utils import timezone
import datetime


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

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField('选项',max_length=200)
    votes = models.IntegerField('票数',default=0)
    class Meta:
        verbose_name = '选项'
        verbose_name_plural = '选项'
    def __str__(self):
        return self.choice_text