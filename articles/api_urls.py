from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ArticleViewSet, CommentViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]

