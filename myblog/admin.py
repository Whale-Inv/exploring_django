from django.contrib import admin

from myblog.models import MyPosts


@admin.register(MyPosts)
class MyPostsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "created_at", "is_published")
    list_filter = ("title",)
    search_fields = ("title", "content")

