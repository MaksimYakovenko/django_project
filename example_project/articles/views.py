from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django import forms
from .models import Article, Category, Comment


class HomeView(ListView):
    template_name = "articles/home.html"
    context_object_name = "articles"
    queryset = Article.objects.filter(is_published=True).select_related(
        "category")[:3]


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = "articles/article_list.html"
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("author", "text")


def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.article = article
            c.save()
    return redirect("articles:detail", pk=pk)


class CategoryListView(ListView):
    model = Category
    template_name = "articles/category_list.html"
    context_object_name = "categories"
