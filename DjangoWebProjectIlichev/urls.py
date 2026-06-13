# -*- coding: utf-8 -*-
"""
Definition of urls for DjangoWebProjectIlichev.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('links/', views.links, name='links'),
    path('registration/', views.registration, name='registration'),
    path('news/', views.news, name='news'),
    path('news/<int:parametr>/', views.newspost, name='newspost'),
    path('newpost/', views.newpost, name='newpost'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('manager/orders/', views.manager_orders, name='manager_orders'),
    path('manager/orders/<int:order_id>/', views.manager_update_order, name='manager_update_order'),
    path('login/',
         LoginView.as_view(
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

# Настройка доступа к медиа-файлам
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()