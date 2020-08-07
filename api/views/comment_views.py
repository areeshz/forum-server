from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.post import Post
from ..models.comment import Comment
from ..serializers import PostSerializer, PostSerializerView, UserSerializer, CommentSerializer, CommentSerializerView

# Create 'Comment' views
# class CommentsIndex(APIView):
#   authentication_classes = ()
#   permission_classes = ()
#
#   def get(self, request):
#     """Index Request"""

class Comments(APIView):
  permission_classes=(IsAuthenticated,)
  serializer_class = CommentSerializer
  def post(self, request):
    """Create Comment"""
    print(request.data)
    # Add user to request object
    request.data['comment']['owner'] = request.user.id
    # Serialize / create 'comment'
    print(request.data['comment']) # Should have body, post, and owner defined at this point (body and post from request itself, owner from line above)
    comment = CommentSerializer(data=request.data['comment'])
    if comment.is_valid():
      comment.save()
      return Response(comment.data, status=status.HTTP_201_CREATED)
    else:
      return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes=(IsAuthenticated,)
  serializer_class = CommentSerializer
  queryset = Comment.objects.all()
  def partial_update(self, request, pk):
    """Update Request"""
    # Remove owner from request object
    if request.data['comment'].get('owner', False):
      del request.data['comment']['owner']

    # Locate Comment
    comment = get_object_or_404(Comment, pk=pk)
    # Check if user is the same
    if not request.user.id == comment.owner.id:
      raise PermissionDenied('Unauthorized, you do not own this comment')

    # Add owner to data object now that we know this user owns the resource
    request.data['comment']['owner'] = request.user.id
    # Validate updates with serializer
    new_comment = CommentSerializer(comment, data=request.data['comment'])
    if new_comment.is_valid():
      new_comment.save()
      return Response(new_comment.data)
    else:
      return Response(new_comment.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    """Delete Request"""
    # Locate the comment
    comment = get_object_or_404(Comment, pk=pk)
    print('reqid', request.user.id, 'commentid', comment.owner.id, 'not owner?', not request.user.id == comment.owner.id)
    if not request.user.id == comment.owner.id:
      raise PermissionDenied('Unauthorized, you do not own this comment')
    else:
      comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
