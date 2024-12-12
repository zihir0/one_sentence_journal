from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(
        validators=[MaxLengthValidator(280, message="Content must be 280 characters or less")]
    )
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likeposts_set.count()

    def comments_count(self):
        return self.comment_set.count()

class LikePosts(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

    class Meta:
        unique_together = ('post', 'user')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(
        validators=[MaxLengthValidator(280, message="Comment must be 280 characters or less")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"