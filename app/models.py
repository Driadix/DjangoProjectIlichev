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