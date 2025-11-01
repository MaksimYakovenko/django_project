from django.contrib import admin
from .models import Article, Category, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "icon")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("title",)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
    "title", "author", "category", "publication_date", "is_published")
    list_filter = ("category", "is_published", "publication_date", "tags")
    search_fields = ("title", "author", "text")
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "article", "publication_date")
    search_fields = ("author", "text")
