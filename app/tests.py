from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from .models import News
from .models import Category, Product


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


class RolesTest(TestCase):

    def test_groups_exist(self):
        self.assertTrue(Group.objects.filter(name='Client').exists())
        self.assertTrue(Group.objects.filter(name='Manager').exists())

    def test_registration_assigns_client_group(self):
        self.client.post('/registration/', {
            'username': 'testuser',
            'password1': 'Str0ngP@ss!',
            'password2': 'Str0ngP@ss!',
        })
        user = User.objects.get(username='testuser')
        self.assertTrue(user.groups.filter(name='Client').exists())
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class CatalogViewTest(TestCase):

    def setUp(self):
        self.cat = Category.objects.create(name='Тест', slug='test', description='Описание')
        self.product = Product.objects.create(
            category=self.cat, name='Товар', description='Описание товара', price='100.00'
        )

    def test_catalog_page(self):
        response = self.client.get('/catalog/')
        self.assertContains(response, 'Каталог', status_code=200)

    def test_category_detail(self):
        response = self.client.get(f'/catalog/{self.cat.slug}/')
        self.assertContains(response, self.cat.name, status_code=200)

    def test_category_404(self):
        response = self.client.get('/catalog/nonexistent/')
        self.assertEqual(response.status_code, 404)

    def test_product_detail(self):
        response = self.client.get(f'/product/{self.product.id}/')
        self.assertContains(response, 'Товар', status_code=200)
        self.assertContains(response, '100')

    def test_product_404(self):
        response = self.client.get('/product/99999/')
        self.assertEqual(response.status_code, 404)
