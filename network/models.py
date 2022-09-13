from operator import mod
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
    content = models.Char

class Followers(models.Model):
    followers = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    followers_number = models.IntegerField(default=0)

class Following(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    following_number = models.IntegerField(default=0)



