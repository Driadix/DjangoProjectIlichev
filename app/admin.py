from django.contrib import admin
from .models import News, Comment, Category, Product, Order, OrderItem


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted', 'image')
    list_filter = ('posted',)
    search_fields = ('title', 'description', 'content')
    ordering = ('-posted',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date')
    list_filter = ('date', 'author')
    search_fields = ('text',)
    ordering = ('-date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('category', 'name')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__username',)
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
