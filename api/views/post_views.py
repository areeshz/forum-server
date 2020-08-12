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
class PostsIndex(generics.ListAPIView):
  authentication_classes = ()
  permission_classes = ()
  queryset = Post.objects.all()

  def get(self, request):
    """Index Request"""
    topic = request.query_params.get('topic', None)
    if topic is not None:
      posts = Post.objects.filter(topic=topic)
    else:
      posts = Post.objects.all()
    data = PostSerializerView(posts, many=True).data
    return Response(data)

class PostsCreate(generics.ListCreateAPIView):
  permission_classes=(IsAuthenticated,)
  serializer_class = PostSerializer
  def post(self, request):
    """Create request"""
    # Add user to request object
    request.data['post']['owner'] = request.user.id
    # Serialize / create 'post'
    post = PostSerializer(data=request.data['post'])
    if post.is_valid():
      post.save()
      return Response(post.data, status=status.HTTP_201_CREATED)
    else:
      return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)

class PostsShow(generics.ListAPIView):
  authentication_classes = ()
  permission_classes = ()

  def get(self, request, pk):
    """Show Request"""
    post = get_object_or_404(Post, pk=pk)
    data = PostSerializerView(post).data
    return Response(data)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes=(IsAuthenticated,)
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  def partial_update(self, request, pk):
    """Update Request"""
    # Remove owner from request object
    if request.data['post'].get('owner', False):
      del request.data['post']['owner']

    # Locate Post
    post = get_object_or_404(Post, pk=pk)
    # Check if user is the same
    if not request.user.id == post.owner.id:
      raise PermissionDenied('Unauthorized, you do not own this post')

    # Add owner to data object now that we know this user owns the resource
    request.data['post']['owner'] = request.user.id
    # Validate updates with serializer
    new_post = PostSerializerView(post, data=request.data['post'])
    if new_post.is_valid():
      new_post.save()
      return Response(new_post.data)
    return Response(new_post.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    """Delete Request"""
    # Locate the post
    post = get_object_or_404(Post, pk=pk)
    if not request.user.id == post.owner.id:
      raise PermissionDenied('Unauthorized, you do not own this post')
    else:
      post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class BaseManageView(APIView):
    """
    The base class for ManageViews
        A ManageView is a view which is used to dispatch the requests to the appropriate views
        This is done so that we can use one URL with different methods (GET, PUT, etc)
    """
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)

        return Response(status=405)

class PostsManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'GET': PostsIndex.as_view,
        'POST': PostsCreate.as_view
    }

class PostDetailManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'GET': PostsShow.as_view,
        'PATCH': PostDetail.as_view,
        'DELETE': PostDetail.as_view
    }
