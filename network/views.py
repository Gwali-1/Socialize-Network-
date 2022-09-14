from importlib.resources import contents
import re
from turtle import pos
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json

from .models import User,Post,Followers,Following


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")












#state changing routes


#new post
@login_required
def new_post(request):
    if request.method == "POST":
        post = request.POST["content"]
        if post:
            try:
                 new_post = Post.objects.create(content=post.strip(),user = request.user)
                 new_post.save()
            except Exception as e:
                print(e)
                return HttpResponse("could not add post: ",e)
        
        return render(request,"network/post.html",{
            "error":"enter valid post"
        })
    
    return render(request,"network/post.html")



#edit
@login_required
@csrf_protect
def edit_post(request):
    if request.method == "POS":
        request_data = json.loads(request.body)
        if request_data.edit:
                try:
                    post = Post.objects.get(id=request_data.id,user=request.user)
                    post.content = request_data.edit.strip()
                    post.save()
                except Post.DoesNotExist:
                    return HttpResponse("could not find post ")
                return JsonResponse(post.serialize(),safe=False)
        return JsonResponse({
            "error":"send a valid edit"
        },status=404)






#like/unlike
@login_required
@csrf_protect
def like_or_unlike(request):
    if request.method == "PUT":
        request_data = json.loads(request.body)
        try:
            post = Post.objects.get(id=request_data.id)
            if request_data.like:
                post.likes = post.likes + 1
                post.save()
                return JsonResponse({
                    "liked":True
                })

            post.likes = post.likes  - 1
            post.save()
            return JsonResponse({

                "liked":False
            })
        except Post.DoesNotExist:
            return HttpResponse("culd not find post")
    return JsonResponse({
        "error":"request must be a PUT request"
    },status=404)
            





#follow/unfollow
def follow_or_unfollow(request):
    if request.method == "PUT":
        request_data = json.loads(request.body)
        try:
            user = User.objects.get(pk=request_data.id)
            if request.user != user:
                if request.data.follow:
                    new_following = Following.objects.create(user=request.user,following=user)
                    new_follower = Followers.objects.create(user=user,follower=request.user)
                    user.followers_number += 1
                    request.user.following_number += 1

                    ##save chamges
                    new_following.save()
                    new_follower.save()
                    user.save()
                    request.user.save()
                    return JsonResponse({
                        "followed":True
                    })
                Following.objects.get(user=request.user ,following=user).delete()
                Followers.objects.get(user=user, follower = request.user).delete()

                return JsonResponse({
                    "followed":False,
                    "user":user.username
                })

            return JsonResponse({
                "error":"Can't follow yourself"
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                "error":"could not follow user at this time"
            },status=404)

    return JsonResponse({
        "error":"request must be a PUT request"
    },status=404)

            

   