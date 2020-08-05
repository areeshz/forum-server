from django.db import models

from .user import User

#Create the 'post' model
class Post(models.Model):
  """Defines the 'post' model"""
  title = models.CharField(max_length=300)
  body = models.CharField(max_length=5000)
  owner = models.ForeignKey(
    'User',
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"Post titled: {self.title}"

  def as_dict(self):
    """Returns dictionary version of Post models"""
    return {
      'id': self.id,
      'title': self.title,
      'body': self.body
    }
