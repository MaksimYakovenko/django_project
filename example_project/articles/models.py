from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100,
                            help_text="FontAwesome class, e.g. fa-solid fa-book")

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=120)  # як звичайний рядок
    text = models.TextField()
    # image = посилання на картинку
    image = models.URLField(blank=True)
    publication_date = models.DateField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name="articles",
                                 on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")

    class Meta:
        ordering = ["-publication_date", "-id"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=120)
    publication_date = models.DateField(default=timezone.now)
    article = models.ForeignKey(Article, related_name="comments",
                                on_delete=models.CASCADE)

    class Meta:
        ordering = ["-publication_date", "-id"]

    def __str__(self):
        return f"{self.author}: {self.text[:30]}..."
