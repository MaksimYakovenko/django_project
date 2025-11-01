from django.urls import path
from .views import HomeView, ArticleListView, ArticleDetailView, add_comment, CategoryListView

app_name = "articles"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="list"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    path("articles/<int:pk>/comment/", add_comment, name="comment"),
    path("categories/", CategoryListView.as_view(), name="categories"),
]
