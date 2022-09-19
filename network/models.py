from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    followers_number = models.IntegerField(default=0)
    following_number = models.IntegerField(default=0)
    joined = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    content = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="post_created")

    def __str__(self):
        return f" {self.content} : user={self.user} "

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "created":self.created,
            "user": self.user
        }

class Likes(models.Model):
    liked_posts = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="liked_posts")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_likes")


class Followers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_followers")
    follower = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.user} followed by {self.follower}"
   

class Following(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_following")
    following = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
         return  f"{self.user} following {self.following}"
   




