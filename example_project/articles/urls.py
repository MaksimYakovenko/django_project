from django.urls import path
from .views import (
    HomeView,
    ArticleListView,
    ArticleDetailView,
    add_comment,
    edit_comment,
    delete_comment,
    CategoryListView,
)

app_name = "articles"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="list"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    path("articles/<int:pk>/comment/", add_comment, name="comment"),
    path("comment/<int:comment_id>/edit/", edit_comment, name="edit_comment"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path("categories/", CategoryListView.as_view(), name="categories"),
]