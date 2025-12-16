from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article, Comment, Category, Tag
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    CategorySerializer,
    TagSerializer
)


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду статей.
    Список статей використовує ArticleListSerializer,
    деталі статті використовують ArticleDetailSerializer з коментарями.
    """
    queryset = Article.objects.filter(is_published=True).select_related('category', 'user').prefetch_related('tags', 'comments')
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint для роботи з коментарями.
    Дозволяє створювати, читати, оновлювати та видаляти коментарі.
    """
    queryset = Comment.objects.all().select_related('article', 'user')
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Якщо користувач авторизований, зберігаємо його
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду категорій.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду тегів.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

