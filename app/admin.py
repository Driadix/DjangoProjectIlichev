from django.contrib import admin
from .models import News, Comment, Category, Product


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
