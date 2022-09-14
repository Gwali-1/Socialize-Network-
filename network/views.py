from importlib.resources import contents
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

