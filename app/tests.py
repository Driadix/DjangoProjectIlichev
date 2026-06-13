from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from .models import News, Category, Product, Order, OrderItem


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
        self.post = News.objects.create(title='Тест', description='Описание', content='Содержание')

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


class CartTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='client1', password='testpass123')
        group = Group.objects.get(name='Client')
        self.user.groups.add(group)
        self.cat = Category.objects.create(name='Кат', slug='kat')
        self.product = Product.objects.create(category=self.cat, name='Товар', description='d', price=Decimal('500.00'))

    def test_cart_requires_login(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 302)

    def test_add_to_cart(self):
        self.client.login(username='client1', password='testpass123')
        response = self.client.get(f'/cart/add/{self.product.id}/')
        self.assertRedirects(response, '/cart/')
        order = Order.objects.get(client=self.user, status='cart')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().price, Decimal('500.00'))

    def test_add_to_cart_twice_increases_quantity(self):
        self.client.login(username='client1', password='testpass123')
        self.client.get(f'/cart/add/{self.product.id}/')
        self.client.get(f'/cart/add/{self.product.id}/')
        order = Order.objects.get(client=self.user, status='cart')
        self.assertEqual(order.items.first().quantity, 2)

    def test_cart_total(self):
        self.client.login(username='client1', password='testpass123')
        self.client.get(f'/cart/add/{self.product.id}/')
        self.client.get(f'/cart/add/{self.product.id}/')
        order = Order.objects.get(client=self.user, status='cart')
        self.assertEqual(order.total(), Decimal('1000.00'))

    def test_remove_from_cart(self):
        self.client.login(username='client1', password='testpass123')
        self.client.get(f'/cart/add/{self.product.id}/')
        item = Order.objects.get(client=self.user, status='cart').items.first()
        self.client.post(f'/cart/update/{item.id}/', {'action': 'remove'})
        order = Order.objects.get(client=self.user, status='cart')
        self.assertEqual(order.items.count(), 0)

    def test_checkout(self):
        self.client.login(username='client1', password='testpass123')
        self.client.get(f'/cart/add/{self.product.id}/')
        self.client.get('/checkout/')
        order = Order.objects.get(client=self.user, status='pending')
        self.assertIsNotNone(order)

    def test_checkout_empty_cart_no_pending(self):
        self.client.login(username='client1', password='testpass123')
        self.client.get('/checkout/')
        self.assertFalse(Order.objects.filter(client=self.user, status='pending').exists())


class MyOrdersTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='client2', password='testpass123')
        group = Group.objects.get(name='Client')
        self.user.groups.add(group)
        self.cat = Category.objects.create(name='К', slug='k')
        self.product = Product.objects.create(category=self.cat, name='Т', description='d', price=Decimal('100.00'))

    def test_my_orders_requires_login(self):
        response = self.client.get('/my-orders/')
        self.assertEqual(response.status_code, 302)

    def test_my_orders_page(self):
        self.client.login(username='client2', password='testpass123')
        response = self.client.get('/my-orders/')
        self.assertContains(response, 'Мои заказы', status_code=200)

    def test_cancel_order(self):
        self.client.login(username='client2', password='testpass123')
        self.client.get(f'/cart/add/{self.product.id}/')
        self.client.get('/checkout/')
        order = Order.objects.get(client=self.user, status='pending')
        self.client.post(f'/my-orders/cancel/{order.id}/')
        order.refresh_from_db()
        self.assertEqual(order.status, 'canceled')

    def test_cannot_cancel_processing_order(self):
        self.client.login(username='client2', password='testpass123')
        self.client.get(f'/cart/add/{self.product.id}/')
        self.client.get('/checkout/')
        order = Order.objects.get(client=self.user, status='pending')
        order.status = 'processing'
        order.save()
        self.client.post(f'/my-orders/cancel/{order.id}/')
        order.refresh_from_db()
        self.assertEqual(order.status, 'processing')


class ManagerOrdersTest(TestCase):

    def setUp(self):
        self.manager = User.objects.create_user(username='mgr', password='testpass123')
        mgr_group = Group.objects.get(name='Manager')
        self.manager.groups.add(mgr_group)

        self.client_user = User.objects.create_user(username='cli', password='testpass123')
        cli_group = Group.objects.get(name='Client')
        self.client_user.groups.add(cli_group)

        self.cat = Category.objects.create(name='М', slug='m')
        self.product = Product.objects.create(category=self.cat, name='Т', description='d', price=Decimal('200.00'))

    def test_manager_page_requires_manager_role(self):
        self.client.login(username='cli', password='testpass123')
        response = self.client.get('/manager/orders/')
        self.assertRedirects(response, '/')

    def test_manager_page_accessible(self):
        self.client.login(username='mgr', password='testpass123')
        response = self.client.get('/manager/orders/')
        self.assertContains(response, 'Управление заказами', status_code=200)

    def test_manager_update_status(self):
        order = Order.objects.create(client=self.client_user, status='pending')
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=self.product.price)
        self.client.login(username='mgr', password='testpass123')
        self.client.post(f'/manager/orders/{order.id}/', {'status': 'processing'})
        order.refresh_from_db()
        self.assertEqual(order.status, 'processing')

    def test_guest_cannot_access_cart(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 302)

    def test_guest_cannot_access_manager(self):
        response = self.client.get('/manager/orders/')
        self.assertEqual(response.status_code, 302)
