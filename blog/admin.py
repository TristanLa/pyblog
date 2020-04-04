from django.contrib import admin
from django.db import models
from blog.models import PostCategory, Post, Comment
from django.forms import Textarea

# Register your models here.
@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "published",
        "create",
        "comments_count",
    )

    list_filter = (
        "category__name",
        "published",
    )
    autocomplete_fields = ["category"]
    formfield_overrides = {
        models.TextField : {"widget": Textarea(attrs={"rows": 20, "cols":90})},
    }

    def comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()
    comments_count.short_description = "# of comments"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "author_name",
        "text",
        "status",
        "moderation_text",
        "created_at",
    )

    list_editable = (
        "status",
        "moderation_text",
    )

    list_filter = ["status",]

    search_fields = ["author_name", "post__title"]