from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")
    image = models.FileField(default='temp.jpg', verbose_name="Путь к картинке")

    def get_absolute_url(self):
        return reverse("newspost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "новость"
        verbose_name_plural = "новости"


class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name="Новость")

    def __str__(self):
        return 'Комментарий %s к %s' % (self.author, self.post)

    class Meta:
        db_table = "Comments"
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии к новостям"
        ordering = ["-date"]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-имя")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Categories"
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.FileField(default='temp.jpg', verbose_name="Изображение")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Products"
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ["name"]


class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Корзина'),
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('canceled', 'Отменён'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Клиент")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return 'Заказ #%s (%s)' % (self.id, self.get_status_display())

    class Meta:
        db_table = "Orders"
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        ordering = ["-created_at"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return '%s x%s' % (self.product.name, self.quantity)

    class Meta:
        db_table = "OrderItems"
        verbose_name = "позиция заказа"
        verbose_name_plural = "позиции заказа"
