from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PostInteractionTypeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = UserSerializer()

    class Meta:
        model = PostInteraction
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = UserSerializer()

    class Meta:
        model = Like
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class GroupMembershipSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    user = UserSerializer()

    class Meta:
        model = GroupMembership
        fields = '__all__'

class CommentReplySerializer(serializers.ModelSerializer):
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    user = UserSerializer()

    class Meta:
        model = CommentReply
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Notification
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tag = TagSerializer()

    class Meta:
        model = Post
        fields = '__all__'
