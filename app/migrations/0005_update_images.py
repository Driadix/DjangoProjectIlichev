# -*- coding: utf-8 -*-
from django.db import migrations

def update_images(apps, schema_editor):
    Blog = apps.get_model('app', 'Blog')

    updates = {
        "Почему мы любим C": "c.jpg",
        "Vim": "vim.jpg",
        "8-бит": "retro.jpg",
        "UNIX": "unix.jpg"
    }

    for key, filename in updates.items():
        post = Blog.objects.filter(title__icontains=key).first()
        if post:
            post.image = filename
            post.save()

def reverse_func(apps, schema_editor):
    Blog = apps.get_model('app', 'Blog')
    Blog.objects.filter(title__in=[
        "Возвращение к истокам: Почему мы любим C",
        "Vim vs Emacs: Вечная война",
        "Эстетика 8-бит: Когда ограничения рождали шедевры",
        "Философия UNIX"
    ]).update(image='temp.jpg')

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_blog_image'),
    ]
    operations = [
        migrations.RunPython(update_images, reverse_func),
    ]