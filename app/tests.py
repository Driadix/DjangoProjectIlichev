from django.test import TestCase
from django.urls import reverse

from .models import News


class ViewTest(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, 'Главная', status_code=200)

    def test_contact(self):
        response = self.client.get('/contact/')
        self.assertContains(response, 'Контакты', status_code=200)

    def test_about(self):
        response = self.client.get('/about/')
        self.assertContains(response, 'О нас', status_code=200)

    def test_links(self):
        response = self.client.get('/links/')
        self.assertContains(response, 'Полезные ресурсы', status_code=200)

    def test_news_page(self):
        response = self.client.get('/news/')
        self.assertContains(response, 'Новости', status_code=200)

    def test_old_blog_url_returns_404(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 404)


class NewsModelTest(TestCase):

    def setUp(self):
        self.post = News.objects.create(
            title='Тест',
            description='Описание',
            content='Содержание',
        )

    def test_str(self):
        self.assertEqual(str(self.post), 'Тест')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), reverse('newspost', args=[str(self.post.id)]))

    def test_ordering(self):
        post2 = News.objects.create(title='Тест2', description='d', content='c')
        posts = list(News.objects.all())
        self.assertEqual(posts[0], post2)


class HomeLatestNewsTest(TestCase):

    def test_home_limits_to_three_news(self):
        for i in range(5):
            News.objects.create(title=f'Доп новость {i}', description='d', content='c')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_news']), 3)


class NewsPostViewTest(TestCase):

    def setUp(self):
        self.post = News.objects.create(title='Пост', description='d', content='c')

    def test_newspost_page(self):
        response = self.client.get(f'/news/{self.post.id}/')
        self.assertContains(response, 'Пост', status_code=200)

    def test_newspost_404(self):
        response = self.client.get('/news/99999/')
        self.assertEqual(response.status_code, 404)
