import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

from django.urls import reverse


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() 返回 False 如果问题是一天前创建的
        """
        time = timezone.now() - datetime.timedelta(days=2)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


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


class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

