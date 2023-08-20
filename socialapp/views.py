from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, generics
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes, throttle_classes
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from rest_framework.views import APIView
from rest_framework import viewsets
from .utils import *
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permisssions import *
from django.db.models import Q,Count
from datetime import timedelta
from django.utils import timezone





class FollowView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can follow

    def post(self, request):
        following_id = request.data.get('following_id')  # Get the ID of the user to follow
        follower_id = request.user.id  # Get the ID of the authenticated user as the follower

        # Check if the follower already follows the user
        if Follow.objects.filter(follower_id=follower_id, following_id=following_id).exists():
            return Response({'error': 'You already follow this user.'}, status=status.HTTP_400_BAD_REQUEST)

        data = {'follower': follower_id, 'following': following_id}
        serializer = FollowSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def unfollow(request):
    try:
        user = request.user
        follower_id = user.id
        following_id = request.data.get('following_id')  # Get the ID of the user to unfollow

        # Check if the follow relationship exists
        follow = Follow.objects.filter(follower_id=follower_id, following_id=following_id).first()
        if follow:
            follow.delete()
            data = {
                'message': 'You have successfully unfollowed the user'
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': 'You are not following this user'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def list_followers_following(request):
    try:
        user = User.objects.get(id=request.user.id)
        action = request.query_params.get('action')  # Get the query parameter 'action'

        if action == 'followers':
            relationships = user.followers_set.all()  # Retrieve the followers using the related name
            data_key = 'followers'
        elif action == 'following':
            relationships = user.following_set.all()  # Retrieve the following using the related name
            data_key = 'following'
        else:
            return Response({'error': 'Invalid action parameter'}, status=status.HTTP_400_BAD_REQUEST)

        user_list = [{'id': relationship.following.id, 'username': relationship.following.username,'firstname':relationship.following.firstname,'lastname':relationship.following.lastname,'profile_url':relationship.following.profile_url}for relationship in relationships]

        data = {
            data_key: user_list
        }
        return Response(data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def group_details(request):
    group_id = request.query_params.get('group_id') 
    try:
        group = Group.objects.get(id=group_id)
        
        # Serialize the group details
        group_serializer = GroupSerializer(group)

        # Get the users belonging to the group
        group_users = group.groupmembership_set.all()
        group_users_serializer = GroupMembershipSerializer(group_users, many=True)

        # Combine the group details and group users data
        response_data = {
            'group': group_serializer.data,
            'group_users': group_users_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    
   



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_group(request):
    payload=request.data
    payload.update({
        'owner':request.user.id
    })
    serializer = GroupSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_group(request):
    group_id = request.data.get('group_id')
    user = request.user

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)


    if GroupMembership.objects.filter(group=group, user=user).exists():
        return Response({'error': 'You are already a member of this group'}, status=status.HTTP_400_BAD_REQUEST)

    membership, created = GroupMembership.objects.get_or_create(group=group, user=user)

    if created:
        group.group_users_count += 1
        group.save()
    

    return Response({'message': 'Joined the group'}, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_group(request):
    group_id = request.data.get('group_id')
    user = request.user

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        membership = GroupMembership.objects.get(group=group, user=user)
        membership.delete()

        if group.group_users_count > 0:
            group.group_users_count -= 1
            group.save()

        return Response({'message': 'Left the group'}, status=status.HTTP_200_OK)
    except GroupMembership.DoesNotExist:
        return Response({'error': 'You are not a member of this group'}, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the requesting user is the owner of the group
    if group.owner != request.user:
        return Response({'error': 'You are not the owner of this group.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response({'message': 'Group deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request):
    query = request.query_params.get('query', '')

    # Search users, posts, and groups using Q objects
    public_users = User.objects.filter(
    Q(username__icontains=query) | Q(firstname__icontains=query) | Q(lastname__icontains=query),
    account_type='public'
    )

    # Filter private users who are followed by request.user
    private_users_followed = User.objects.filter(
        Q(username__icontains=query) | Q(firstname__icontains=query) | Q(lastname__icontains=query),
        account_type='private',
        followers_set__follower=request.user  # Assuming 'followers_set' is the related name
    )

    # Combine the two querysets
    users = public_users | private_users_followed

    # Get posts matching the search query with audience type 'public'
    public_posts = Post.objects.filter(
        Q(post_text__icontains=query),
        audience_type=Post.PUBLIC
    )

    # Get private posts by users followed by request.user
    private_posts_visible = Post.objects.filter(
        Q(post_text__icontains=query),
        audience_type=Post.PRIVATE,
        user__in=request.user.following_set.values('following')
    )
    # Combine the two querysets
    posts = public_posts | private_posts_visible

    groups = Group.objects.filter(Q(group_name__icontains=query) | Q(group_description__icontains=query))

    # Serialize the search results
    user_serializer = UserSerializer(users, many=True)
    post_serializer = PostSerializer(posts, many=True)
    group_serializer = GroupSerializer(groups, many=True)

    response_data = {
        'users': user_serializer.data,
        'posts': post_serializer.data,
        'groups': group_serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)



class TrendingAndPopularPostsView(APIView):
    def get(self, request):
        # Trending Posts: Retrieve posts with high interaction_count
        trending_posts = Post.objects.filter(interaction_count__gt=0).order_by('-interaction_count')[:10]
      

        # Popular Posts: Retrieve posts with high interaction_count within the last week
        last_week = timezone.now() - timedelta(days=7)
        popular_posts = Post.objects.filter(interaction_count__gt=0, created_at__gte=last_week).annotate(
            total_interactions=Count('interaction_count')
        ).order_by('-total_interactions')[:10]

        # Serialize the results
        trending_serializer = PostSerializer(trending_posts, many=True)
        popular_serializer = PostSerializer(popular_posts, many=True)

        response_data = {
            'trending_posts': trending_serializer.data,
            'popular_posts': popular_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)




class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostInteractionViewSet(viewsets.ModelViewSet):
    queryset = PostInteraction.objects.all()
    serializer_class = PostInteractionTypeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer








class GroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer


class CommentReplyViewSet(viewsets.ModelViewSet):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
