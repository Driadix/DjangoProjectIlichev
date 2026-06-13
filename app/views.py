from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import BootstrapUserCreationForm, CommentForm, NewsForm
from .models import News, Comment, Category, Product, Order, OrderItem


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


def catalog(request):
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()
    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Каталог',
            'categories': categories,
            'year': datetime.now().year,
        }
    )


def category_detail(request, slug):
    assert isinstance(request, HttpRequest)
    cat = get_object_or_404(Category, slug=slug)
    products = cat.products.all()
    return render(
        request,
        'app/category.html',
        {
            'title': cat.name,
            'category': cat,
            'products': products,
            'year': datetime.now().year,
        }
    )


def product_detail(request, pk):
    assert isinstance(request, HttpRequest)
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        'app/product.html',
        {
            'title': product.name,
            'product': product,
            'year': datetime.now().year,
        }
    )


def _get_or_create_cart(user):
    order, _ = Order.objects.get_or_create(client=user, status='cart')
    return order


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = _get_or_create_cart(request.user)
    item, created = OrderItem.objects.get_or_create(
        order=cart, product=product,
        defaults={'price': product.price}
    )
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')


@login_required
def cart_detail(request):
    assert isinstance(request, HttpRequest)
    cart = Order.objects.filter(client=request.user, status='cart').first()
    items = cart.items.select_related('product').all() if cart else []
    total = cart.total() if cart else 0
    return render(
        request,
        'app/cart.html',
        {
            'title': 'Корзина',
            'cart': cart,
            'items': items,
            'total': total,
            'year': datetime.now().year,
        }
    )


@login_required
def cart_update(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__client=request.user, order__status='cart')
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'increase':
            item.quantity += 1
            item.save()
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        elif action == 'remove':
            item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    cart = Order.objects.filter(client=request.user, status='cart').first()
    if cart and cart.items.exists():
        cart.status = 'pending'
        cart.save()
    return redirect('my_orders')


@login_required
def my_orders(request):
    assert isinstance(request, HttpRequest)
    orders = Order.objects.filter(client=request.user).exclude(status='cart').select_related('client')
    return render(
        request,
        'app/my_orders.html',
        {
            'title': 'Мои заказы',
            'orders': orders,
            'year': datetime.now().year,
        }
    )


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user)
    if order.status == 'pending':
        order.status = 'canceled'
        order.save()
    return redirect('my_orders')


@login_required
def manager_orders(request):
    assert isinstance(request, HttpRequest)
    if not request.user.groups.filter(name='Manager').exists():
        return redirect('home')
    orders = Order.objects.exclude(status='cart').select_related('client')
    return render(
        request,
        'app/manager_orders.html',
        {
            'title': 'Управление заказами',
            'orders': orders,
            'year': datetime.now().year,
        }
    )


@login_required
def manager_update_order(request, order_id):
    if not request.user.groups.filter(name='Manager').exists():
        return redirect('home')
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in ('processing', 'completed', 'canceled'):
            order.status = new_status
            order.save()
    return redirect('manager_orders')