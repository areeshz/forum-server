from django.db import models

class Like(models.Model):
  # fields for the user and the post to be related by a like
  user_id = models.ForeignKey('User', on_delete=models.CASCADE)
  post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"User {self.user_id} likes Post {self.post_id}"
