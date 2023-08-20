from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'comment-replies', CommentReplyViewSet)
router.register(r'post-interactions', PostInteractionViewSet)
router.register(r'group-memberships', GroupMembershipViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'follows', FollowView)


urlpatterns = [
    path('follow', FollowView.as_view(), name="follow"),
    path('unfollow', unfollow, name="unfollow"),
    path('following-followers-list', list_followers_following, name="following-followers-list"),
    path('create-group', create_group, name="create_group"),
    path('group_details', group_details, name="group_details"),
    path('join-group', join_group, name="join-group"),
    path('', include(router.urls))
]
