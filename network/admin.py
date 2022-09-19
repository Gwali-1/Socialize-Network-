from atexit import register
from django.contrib import admin
from .models import User,Post,Followers,Following,Likes


# Register your models here.

class Useradmin(admin.ModelAdmin):
    list_display = ("id","first_name","username","followers_number","following_number")


class Postadmin(admin.ModelAdmin):
    list_display = ("id","user","created","likes")

class Followersadmin(admin.ModelAdmin):
    list_display = ("id","user","follower")

class Followingadmin(admin.ModelAdmin):
    list_display = ("id","user","following")

class Likesadmin(admin.ModelAdmin):
    list_display =("id","user","liked_posts")

admin.site.register(User)
admin.site.register(Likes,Likesadmin)
admin.site.register(Post)
admin.site.register(Followers,Followersadmin)
admin.site.register(Following,Followingadmin)