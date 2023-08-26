from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.views import *

from .views import *


router = DefaultRouter()
router.register(r'tags', TagViewSet)
# router.register(r'posts', PostViewSet)
# router.register(r'likes', LikeViewSet)
# router.register(r'comments', CommentViewSet)
# router.register(r'comment-replies', CommentReplyViewSet)
# router.register(r'post-interactions', PostInteractionViewSet)
# router.register(r'group-memberships', GroupMembershipViewSet)
# router.register(r'notifications', NotificationViewSet)
# router.register(r'follows', FollowView)


urlpatterns = [
    path('follow', FollowView.as_view(), name="follow"),
    path('unfollow', unfollow, name="unfollow"),
    path('following-followers-list', list_followers_following,
         name="following-followers-list"),
    path('post/like_unlike_post/<int:post_id>/',
         like_unlike_post, name="like_unlike_post"),
    path('post/get_posts', get_posts, name="get_posts"),
    path('post/create_post', create_post, name="create_post"),
    path('post/edit-post/<int:post_id>', edit_post, name='edit-post'),
    path('post/delete-post/<int:post_id>', delete_post, name='delete-post'),
    path('post/posts/<int:post_id>/comments',
         get_comments_for_post, name='get_comments_for_post'),
    path('posts/<int:post_id>/comments', create_comment, name='create_comment'),
    path('comments/<int:comment_id>', delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/replies',
         get_comment_replies, name='get_comment_replies'),
    path('comments/<int:comment_id>/replies',
         create_comment_reply, name='create_comment_reply'),
    path('comments/<int:comment_id>/replies/<int:reply_id>',
         delete_comment_reply, name='delete_comment_reply'),
    path('post/shared-posts', get_shared_posts, name='get_shared_posts'),
    path('shared-posts/<int:post_share_id>', delete_shared_post, name='delete_shared_post'),
         
    # path('following-followers-list', list_followers_following, name="following-followers-list"),
    path('group/create-group', create_group, name="create_group"),
    path('group/group_details', group_details, name="group_details"),
    path('group/join-group', join_group, name="join-group"),
    path('group/leave-group', leave_group, name="join-leave_group"),
    path('group/edit-delete-group/<int:group_id>/', edit_delete_group, name="edit_delete_group"),
    path('search/', search, name='search'),
    path('post/trending-popular-posts/', TrendingAndPopularPostsView.as_view(), name='trending-popular-posts'),
    path('', include(router.urls))
]
