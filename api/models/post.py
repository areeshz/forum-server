from django.db import models

from .user import User

#Create the 'post' model
class Post(models.Model):
  """Defines the 'post' model"""
  title = models.CharField(max_length=300)
  body = models.CharField(max_length=5000)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner = models.ForeignKey(
    'User',
    on_delete=models.CASCADE
  )

  GENERAL = 'General'
  SPORTS = 'Sports'
  CURRENT_EVENTS = 'Current Events'
  ADVICE = 'Advice'
  PETS = 'Pets'
  BOOKS = 'Books'
  MOVIE_TV = 'Movies / TV'
  TOPIC_CHOICES = [
    (GENERAL, 'General'),
    (SPORTS, 'Sports'),
    (CURRENT_EVENTS, 'Current Events'),
    (ADVICE, 'Advice'),
    (PETS, 'Pets'),
    (BOOKS, 'Books'),
    (MOVIE_TV, 'Movies / TV')
  ]

  topic = models.CharField(
    max_length=25,
    choices=TOPIC_CHOICES,
    default=GENERAL
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
