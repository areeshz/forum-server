from django.db import models

from .user import User
from .post import Post

# Create the 'comment' model
class Comment(models.Model):
  """Defines the 'comment' model"""
  body = models.CharField(max_length=3000)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  owner = models.ForeignKey(
    'User',
    on_delete=models.CASCADE
  )

  post = models.ForeignKey(
    'Post',
    related_name='comments',
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"Comment on post {self.post}, body {self.body}"

  def as_dict(self):
    """Returns dictionary version of Comment models"""
    return {
      'id': self.id,
      'body': self.body,
      'post': self.post,
      'owner': self.owner
    }
