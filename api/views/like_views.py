from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models.like import Like
from ..serializers import LikeSerializer

class Likes(APIView):
  permission_classes=(IsAuthenticated,)
  def get(self, request):
    """Index Request"""
    likes = Like.objects.all()
    data = LikeSerializer(likes, many=True).data
    return Response(data)

  def post(self, request):
    """Create Request"""
    # Set user_id from request user to the request object, to ensure a user can only make a 'like' on their own behalf
    request.data['like']['user_id'] = request.user.id
    like = request.data['like']
    new_like = LikeSerializer(data=like)
    # Check if a like exists already between this user and post
    current_like = Like.objects.filter(user_id=request.user.id, post_id=request.data['like']['post_id'])
    current_like_data = LikeSerializer(current_like, many=True).data
    # return Response(status=status.HTTP_204_NO_CONTENT)
    # if the new like is valid and there are no existing likes between this user and post, save the new like
    if (new_like.is_valid() and not current_like_data):
      new_like.save()
      return Response(new_like.data, status=status.HTTP_201_CREATED)
    else:
      return Response(new_like.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request):
    """Delete Request"""
    # Locate the like that corresponds to the user and the provided post id
    like = get_object_or_404(Like, user_id=request.user.id, post_id=request.data['post_id'])
    data = LikeSerializer(like).data
    if not request.user.id == data['user_id']:
      raise PermissionDenied('Unauthorized, you have not \'liked\' this post.')
    else:
      like.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class LikeDetail(APIView):
  def get(self, reques, pk):
    """Show Request"""
    like = get_object_or_404(Like, pk=pk)
    data = LikeSerializer(like).data
    return Response(data, status=status.HTTP_200_OK)
