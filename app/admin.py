from django.contrib import admin
from .models import News, Comment


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
