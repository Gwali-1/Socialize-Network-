from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers_number = models.IntegerField(default=0)
    following_number = models.IntegerField(default=0)



class Post(models.Model):
    content = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="post_created")



class Followers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_followers")
    follower = models.ForeignKey(User,on_delete=models.CASCADE)
   

class Following(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_following")
    following = models.ForeignKey(User,on_delete=models.CASCADE)




