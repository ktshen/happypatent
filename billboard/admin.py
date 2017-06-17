from django.contrib import admin

from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]



