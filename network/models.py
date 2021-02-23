from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# extending the user profile to add a profile picture
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    bio = models.CharField(blank=True, max_length=400)
    profile_picture = models.ImageField(blank=True, upload_to="network/images/", default="images/no-image.jpg")


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user", default=1)
    content = models.TextField(max_length=450)
    # likes = models.ForeignKey(Like, on_delete=models.CASCADE, related_name="post_likes", default=0)
    likes = models.ManyToManyField(User, blank=True)
    # likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "likes": [user.username for user in self.likes.all()],
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p")
        }

class Like(models.Model):
    user = models.ManyToManyField(User)
    post = models.ManyToManyField(Post)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_user", default=1)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked", default=1)
    liked = models.BooleanField()
    
class Following(models.Model):
    # idea
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_user", default=1)
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user", default=1)
    following = models.BooleanField()
