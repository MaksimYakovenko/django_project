from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["is_moderator"] = (
                user.is_authenticated and user.groups.filter(
            name="moderator").exists()
        )
        return context


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("author", "text")


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user and not request.user.groups.filter(
            name="moderator").exists():
        return HttpResponseForbidden(
            "Ви не маєте прав для редагування цього коментаря.")
    if request.method == "POST":
        new_text = request.POST.get("text", "").strip()
        if new_text:
            comment.text = new_text
            comment.save()
            return redirect("articles:detail", pk=comment.article.id)
    return render(request, "articles/edit_comment.html", {"comment": comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user and not request.user.groups.filter(
            name="moderator").exists():
        return HttpResponseForbidden(
            "Ви не маєте прав для видалення цього коментаря.")
    article_pk = comment.article.pk
    comment.delete()
    return redirect("articles:detail", pk=article_pk)


def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            comment = Comment(article=article, text=text)
            if request.user.is_authenticated:
                comment.user = request.user
                comment.author = request.user.get_username()
            else:
                author_name = request.POST.get("author_name", "").strip()
                comment.author = author_name or "Анонім"
            comment.save()
    return redirect("articles:detail", pk=pk)


class CategoryListView(ListView):
    model = Category
    template_name = "articles/category_list.html"
    context_object_name = "categories"
