from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.mango import Mango
from .models.user import User
from .models.post import Post
from .models.comment import Comment


class MangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mango
        fields = ('id', 'name', 'color', 'ripe', 'owner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)

class UserSerializerView(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email')

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    # fields = ('id', 'title', 'body', 'owner')
    fields = '__all__'

class PostSerializerView(serializers.ModelSerializer):
    owner = UserSerializerView(read_only=True)
    class Meta:
      model = Post
      fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

class CommentSerializerView(serializers.ModelSerializer):
  owner = UserSerializerView(read_only=True)
  post = PostSerializerView(read_only=True)
  class Meta:
    model = Comment
    fields = '__all__'
