from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'tags', TagViewSet)
# router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'comment-replies', CommentReplyViewSet)
router.register(r'post-interactions', PostInteractionViewSet)
router.register(r'group-memberships', GroupMembershipViewSet)
router.register(r'notifications', NotificationViewSet)
# router.register(r'follows', FollowView)


urlpatterns = [
    path('follow', FollowView.as_view(), name="follow"),
    path('unfollow', unfollow, name="unfollow"),
    path('following-followers-list', list_followers_following,
         name="following-followers-list"),
    path('create-group', create_group, name="create_group"),
    path('group_details', group_details, name="group_details"),
    path('like_unlike_post/<int:post_id>/',
         like_unlike_post, name="like_unlike_post"),
    path('join-group', join_group, name="join-group"),
    path('get_posts', get_posts, name="get_posts"),
    path('create_post', create_post, name="create_post"),
    path('edit-post/<int:post_id>', edit_post, name='edit-post'),
    path('delete-post/<int:post_id>', delete_post, name='delete-post'),
    path('posts/<int:post_id>/comments',
         get_comments_for_post, name='get_comments_for_post'),
    path('posts/<int:post_id>/comments', create_comment, name='create_comment'),
    path('comments/<int:comment_id>', delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/replies',
         get_comment_replies, name='get_comment_replies'),
    path('comments/<int:comment_id>/replies',
         create_comment_reply, name='create_comment_reply'),
    path('comments/<int:comment_id>/replies/<int:reply_id>',
         delete_comment_reply, name='delete_comment_reply'),
    path('', include(router.urls))
]
