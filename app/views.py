# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Связь с администрацией узла.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Информация о нашем клубе.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Избранные ссылки сети.',
            'year':datetime.now().year,
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            reg_f.save()

            return redirect('home')
    else:
        regform = UserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )