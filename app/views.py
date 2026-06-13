from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.models import Group
from .forms import BootstrapUserCreationForm, CommentForm, NewsForm
from .models import News, Comment


def home(request):
    assert isinstance(request, HttpRequest)
    latest_news = News.objects.order_by('-posted')[:3]
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'latest_news': latest_news,
            'year': datetime.now().year,
        }
    )


def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Связь с администрацией узла.',
            'year': datetime.now().year,
        }
    )


def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'message': 'Информация о нашем клубе.',
            'year': datetime.now().year,
        }
    )


def links(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'message': 'Избранные ссылки сети.',
            'year': datetime.now().year,
        }
    )


def registration(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        regform = BootstrapUserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            client_group = Group.objects.get(name='Client')
            reg_f.groups.add(client_group)
            return redirect('home')
    else:
        regform = BootstrapUserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )


def news(request):
    assert isinstance(request, HttpRequest)
    posts = News.objects.order_by('-posted')
    return render(
        request,
        'app/news.html',
        {
            'title': 'Новости',
            'posts': posts,
            'year': datetime.now().year,
        }
    )


def newspost(request, parametr):
    assert isinstance(request, HttpRequest)
    post_1 = get_object_or_404(News, id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()
            return redirect('newspost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/newspost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )


def newpost(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            post_f = form.save(commit=False)
            post_f.posted = datetime.now()
            post_f.save()
            return redirect('news')
    else:
        form = NewsForm()

    return render(
        request,
        'app/newpost.html',
        {
            'form': form,
            'title': 'Добавить новость',
            'year': datetime.now().year,
        }
    )