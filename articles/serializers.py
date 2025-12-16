from rest_framework import serializers
from .models import Article, Comment, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'icon']


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'user', 'user_username', 'publication_date', 'article']
        read_only_fields = ['user', 'publication_date']


class ArticleListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'user_username', 'publication_date',
                  'category', 'category_name', 'comments_count', 'text', 'image']

    def get_comments_count(self, obj):
        return obj.comments.count()


class ArticleDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'user', 'user_username', 'text',
                  'image', 'publication_date', 'is_published', 'category',
                  'category_name', 'tags', 'comments']
        read_only_fields = ['user', 'publication_date']

