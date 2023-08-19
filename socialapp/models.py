from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager
import datetime
from django.db import transaction


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user realization based on Django AbstractUser and PermissionMixin.
    """
    email = models.EmailField(
        ('email address'),
        unique=True,
        blank=True,
        error_messages={
            'unique': ("A user with that email already exists."),
        })
    username = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin '
                   'site.'))
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=('Designates whether this user should be treated as '
                   'active. Unselect this instead of deleting accounts.'))

    password = models.TextField(null=True, blank=True)
    is_firsttime = models.BooleanField(default=True)
    emailverified = models.BooleanField(default=False)
    following_count = models.IntegerField(default=0, blank=True, null=True)
    follower_count = models.IntegerField(default=0, blank=True, null=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        managed = True
        abstract = False
        db_table = 'auth_user'

    def _str_(self):
        return self.email


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.tag_name


class Post(models.Model):

    PUBLIC = "public"
    PRIVATE = "private"
    GROUP = "group"

    AUDIENCE_CHOICES = (
        (PUBLIC, "public"),
        (PRIVATE, "private"),
        (GROUP, "group"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post_text = models.TextField(blank=True)
    post_image_url = models.CharField(max_length=200, blank=True)
    post_video_url = models.CharField(max_length=200, blank=True)
    interraction_count = models.IntegerField(default=0, blank=True)
    audience_type = models.CharField(
        max_length=10,
        choices=AUDIENCE_CHOICES,
        default=PUBLIC,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostInteractionType(models.Model):
    LIKE = "like"
    COMMENT = "comment"

    INTERACTION_CHOICES = (
        (LIKE, "Like"),
        (COMMENT, "Comment"),
    )

    interaction_type = models.CharField(
        max_length=10,
        choices=INTERACTION_CHOICES,
        default=LIKE,
    )
    interaction_text = models.TextField(blank=True)
    interaction_media = models.TextField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_interaction_type_display()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_description = models.TextField(blank=True)
    group_count = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
