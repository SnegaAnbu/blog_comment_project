from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'is_published']
        read_only_fields = ['author', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Show the username of the comment author

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'post']
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user
