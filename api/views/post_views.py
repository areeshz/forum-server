from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.post import Post
from ..serializers import PostSerializer, PostSerializerView, UserSerializer

# Create 'Post' views
class PostsIndex(generics.ListCreateAPIView):
  authentication_classes = ()
  permission_classes = ()
  serializer_class = PostSerializer
  queryset = Post.objects.all()

  def get(self, request):
    """Index Request"""
    posts = Post.objects.all()
    data = PostSerializerView(posts, many=True).data
    return Response(data)

class PostsCreate(generics.ListCreateAPIView):
  permission_classes=(IsAuthenticated,)
  serializer_class = PostSerializer
  def post(self, request):
    """Create request"""
    print(request.data)
    # Add user to request object
    request.data['post']['owner'] = request.user.id
    # Serialize / create 'post'
    print(request.data['post'])
    post = PostSerializer(data=request.data['post'])
    if post.is_valid():
      post.save()
      return Response(post.data, status=status.HTTP_201_CREATED)
    else:
      return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)
