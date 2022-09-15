from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator

from .models import User,Post,Followers,Following


def index(request):
    if not  request.user.is_authenticated:
        return render(request,"network/login.html",{
            "error":"Session expired ,Login again"
        })
    return HttpResponseRedirect(reverse("all_post",args=(1,)))

    


#login
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




#logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))




#register
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





#all post
@login_required
def all_post(request,page_num):

    if not  request.user.is_authenticated:
        return render(request,"network/login.html",{
            "error":"Session expired ,Login again"
        })


    all_post = Post.objects.all().order_by("-created")
    pages = Paginator(all_post,10)  # show 10 post per page

    if page_num > pages.num_pages:
        return HttpResponse("error")
    try:
        current_page = pages.get_page(page_num)
        print("yes")
        return render(request, "network/all_post.html",{
            "current_page":current_page,
            "number_of_pages":pages.num_pages
        })
    except Exception as e:
        print(e)







#following
def following(request,page_num):

    if not  request.user.is_authenticated:
        return render(request,"network/login.html",{
            "error":"Session expired ,Login again"
        })
    
    users_following = Following.objects.filter(user=request.user)
    user_set = [user for user in users_following]
    following_post = Post.objects.filter(user__in= user_set).order_by("-created")

    pages = Paginator(following_post,10)

    if page_num > pages.num_pages:
            return HttpResponse("error")


    if not  request.user.is_authenticated:
        return render(request,"network/index.html",{
            "error":"Session expired ,Login again"
        })
    try:
        current_page = pages.get_page(page_num)
        return render(request,"network/following.html",{
            "post":current_page
        })
    except Exception as e:
        print(e)
  






#new post
@login_required
def new_post(request):
    if request.method == "POST":
        post = request.POST["content"]
        if post:
            try:
                 new_post = Post.objects.create(content=post.strip(),user = request.user)
                 new_post.save()
                 return HttpResponseRedirect(reverse("index",args=(1,)))
            except Exception as e:
                print(e)
                return HttpResponse("could not add post: ",e)
        
        return render(request,"network/post.html",{
            "error":"enter valid post"
        })
    return render(request, "network/post.html")
    
  


#profile
@login_required
def profile(request):
    
    if not  request.user.is_authenticated:
        return render(request,"network/login.html",{
            "error":"Session expired ,Login again"
        })


    user_post = Post.objects.filter(user=request.user).order_by("-created")
    user = request.user

    return render(request,"network/profile.html",{
        "user_post":user_post,
        "user" : user
    })
























#state changing routes

#edit
@csrf_protect
@login_required
def edit_post(request):
    if request.method == "PUT":
        request_data = json.loads(request.body)
        if request_data.edited:
                try:
                    post = Post.objects.get(id=request_data.id,user=request.user)
                    post.content = request_data.edited.strip()
                    post.save()
                except Post.DoesNotExist:
                    return HttpResponse("could not find post ")
                return JsonResponse(post.serialize(),safe=False)
        return JsonResponse({
            "error":"send a valid edit"
        },status=404)






#like/unlike
@csrf_protect
@login_required
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
@csrf_protect
@login_required
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

            

   