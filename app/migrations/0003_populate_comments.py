from django.db import migrations
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password

def populate_comments(apps, schema_editor):
    Blog = apps.get_model('app', 'Blog')
    Comment = apps.get_model('app', 'Comment')
    User = apps.get_model('auth', 'User')

    # 1. Создаем пользователей
    users_data = [
        {'username': 'neo', 'password': 'matrix123', 'email': 'neo@matrix.net'},
        {'username': 'morpheus', 'password': 'matrix123', 'email': 'morpheus@matrix.net'},
        {'username': 'trinity', 'password': 'matrix123', 'email': 'trinity@matrix.net'},
    ]
    
    user_objects = {}
    for user_info in users_data:
        user, created = User.objects.get_or_create(
            username=user_info['username'],
            defaults={
                'email': user_info['email'],
                'password': make_password(user_info['password']),
                'is_active': True,
                'is_staff': False,
                'is_superuser': False
            }
        )
        user_objects[user_info['username']] = user

    # 2. Находим статьи
    c_post = Blog.objects.filter(title__contains="C").first()
    vim_post = Blog.objects.filter(title__contains="Vim").first()
    retro_post = Blog.objects.filter(title__contains="8-бит").first()

    # 3. Создаем комментарии
    comments_list = []
    
    if c_post:
        comments_list.append(Comment(
            post=c_post,
            author=user_objects['neo'],
            text="Указатели - это путь к пониманию Матрицы.",
            date=datetime.now() - timedelta(days=1)
        ))
        comments_list.append(Comment(
            post=c_post,
            author=user_objects['morpheus'],
            text="Ты думаешь, это воздух, которым ты дышишь? Это память, которой ты управляешь.",
            date=datetime.now()
        ))

    if vim_post:
        comments_list.append(Comment(
            post=vim_post,
            author=user_objects['trinity'],
            text=":q! - это всё, что нужно знать.",
            date=datetime.now() - timedelta(hours=5)
        ))
        comments_list.append(Comment(
            post=vim_post,
            author=user_objects['neo'],
            text="Я знаю кунг-фу... и как выйти из Vim.",
            date=datetime.now()
        ))

    if retro_post:
        comments_list.append(Comment(
            post=retro_post,
            author=user_objects['morpheus'],
            text="Добро пожаловать в реальный мир. 640 килобайт хватит всем.",
            date=datetime.now()
        ))

    Comment.objects.bulk_create(comments_list)

def reverse_func(apps, schema_editor):
    Comment = apps.get_model('app', 'Comment')
    Comment.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_populate_blog'),
    ]

    operations = [
        migrations.RunPython(populate_comments, reverse_func),
    ]