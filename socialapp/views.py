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

from rest_framework import viewsets




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
@permission_classes([IsAuthenticated])
def group_details(request):
    group_id = request.query_params.get('group_id') 
    try:
        group = Group.objects.get(id=group_id)
        ser=GroupSerializer(group)
        return Response(ser.data, status=status.HTTP_201_CREATED)
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

        if group.group_count > 0:
            group.group_count -= 1
            group.save()

        return Response({'message': 'Left the group'}, status=status.HTTP_200_OK)
    except GroupMembership.DoesNotExist:
        return Response({'error': 'You are not a member of this group'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsGroupCreator])  # Apply IsGroupCreator permission
def edit_delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response({'message': 'Group deleted successfully'}, status=status.HTTP_204_NO_CONTENT)







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
