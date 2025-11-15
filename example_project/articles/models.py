from django.db import models
from django.utils import timezone
from django.conf import settings


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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="articles",
        on_delete=models.SET_NULL,
        help_text="Registered user who authored the article",
    )
    author = models.CharField(max_length=120, blank=True)
    text = models.TextField()
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="comments",
        on_delete=models.SET_NULL,
        help_text="Registered user who authored the comment",
    )
    author = models.CharField(max_length=120, blank=True)
    publication_date = models.DateField(default=timezone.now)
    article = models.ForeignKey(
        Article,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-publication_date", "-id"]

    def __str__(self):
        return f"{self.author}: {self.text[:30]}..."
