from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Comment, Post


User = get_user_model()


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    comments = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='comment-detail',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ['url', 'author', 'title', 'body', 'status', 'publish', 'comments']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['url', 'author', 'post', 'body']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
