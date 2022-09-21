from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator

from .models import User,Post,Followers,Following,Likes


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
@login_required
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
    user_likes  = Likes.objects.filter(user=request.user)
    user_liked_post = [x.liked_posts for x in user_likes]
    pages = Paginator(all_post,10)  # show 10 post per page

    if page_num > pages.num_pages:
        return HttpResponseRedirect(reverse("index"))
    try:
        current_page = pages.get_page(page_num)
      
        return render(request, "network/all_post.html",{
            "current_page":current_page,
            "number_of_pages":pages.num_pages,
            "liked_posts":user_liked_post
        })
    except Exception as e:
        return HttpResponseRedirect(reverse("index"))
   

















#following
@login_required
def following(request,page_num):

    if not  request.user.is_authenticated:
        return render(request,"network/login.html",{
            "error":"Session expired ,Login again"
        })
    
    users_following = Following.objects.filter(user=request.user)

    user_likes  = Likes.objects.filter(user=request.user)
    user_liked_post = [x.liked_posts for x in user_likes]

    user_set = [user.following for user in users_following]
    following_post = Post.objects.filter(user__in= user_set).order_by("-created")

    pages = Paginator(following_post,10)

    if page_num > pages.num_pages:
            return HttpResponseRedirect(reverse("index"))


    if not  request.user.is_authenticated:
        return render(request,"network/index.html",{
            "error":"Session expired ,Login again"
        })
    try:
        current_page = pages.get_page(page_num)
        return render(request,"network/following.html",{
            "current_page":current_page,
             "liked_posts":user_liked_post
        })
    except Exception as e:
        return HttpResponseRedirect(reverse("index"))
  


















#new post
@login_required
def new_post(request):
    if request.method == "POST":
        post = request.POST["content"]
        if post:
            try:
                 new_post = Post.objects.create(content=post,user = request.user)
                 new_post.save()
                 return HttpResponseRedirect(reverse("index"))
            except Exception as e:
                return render(request,"network/post.html",{
                    "error":"something went wrong, could not add post at this time"
        })
        return render(request,"network/post.html",{
            "error":"enter valid post"
        })
    return render(request, "network/post.html")
    
  














#profile
@login_required
def profile(request,id,page_num):
    
    if not  request.user.is_authenticated:
        return render(request,"network/login.html",{
            "error":"Session expired ,Login again"
        })

    try:
        
        user_p = User.objects.get(pk=id)
        user_post = Post.objects.filter(user=user_p).order_by("-created")

        user_likes  = Likes.objects.filter(user=request.user)
        user_liked_post = [x.liked_posts for x in user_likes]


        pages = Paginator(user_post,10)
        current_pages = pages.get_page(page_num)
        if user_p in [x.following for x in request.user.user_following.all()]:
            return render(request,"network/profile.html",{
            "user_post":current_pages,
            "user_profile" : user_p,
            "following": "true",
            "liked_posts":user_liked_post
            })

        return render(request,"network/profile.html",{
        "user_post":current_pages,
        "user_profile" : user_p,
        "liked_posts":user_liked_post
    })
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

  

   
























#state changing routes




#like/unlike
@csrf_protect
@login_required
def like_or_unlike(request):
    if request.method == "PUT":
        request_data = json.loads(request.body)
        try:
            post = Post.objects.get(id=request_data.get("id"))

            #if user wants to like
            if request_data.get("like") == "true":
                try:
                    post.likes = post.likes + 1

                    #check if post is liked
                    if(Likes.objects.filter(user=request.user,liked_posts=post)):
                        return JsonResponse({
                            "error":"you already liked post"
                        })
                   


                    new_like = Likes.objects.create(user=request.user,liked_posts=post)
                    new_like.save()
                    post.save()
                    return JsonResponse({
                        "liked":True,
                        "current_likes": post.likes,
                        "post_id": post.id
                    })
                except Exception as e:
                    return  JsonResponse({
                        "error":"something happened,could not like post at this time"
                    })



            #if user want to unlike
            try:

                Likes.objects.get(user=request.user,liked_posts=post).delete()
                post.likes = post.likes  - 1
                post.save()
                return JsonResponse({
                    "liked":False,
                    "current_likes": post.likes,
                    "post_id": post.id
                })
            except Exception as e:
                return JsonResponse({
                    "error":"something went wrong"
                })
        except Post.DoesNotExist:
            return JsonResponse({
                    "error":"something went wrong,could not like post"
                })
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
            user = User.objects.get(pk=request_data.get("id"))

           

            if request.user != user:
                if request_data.get("follow"):
                 #if user is already followed 
                    check = Following.objects.filter(user=request.user,following=user)
                    if check:
                        return JsonResponse({
                        "error":"you already follow user",
                     })

                    try:
                        new_following = Following.objects.create(user=request.user,following=user)
                        new_follower = Followers.objects.create(user=user,follower=request.user)
                        user.followers_number += 1
                       

                        ##save chamges
                        new_following.save()
                        new_follower.save()
                        user.save()
                        request.user.save()
                        return JsonResponse({
                            "followed":True,
                            "current_followers" :user.followers_number
                        })
                    except Exception as e:
                        return JsonResponse({
                            "error":"could not follow user at this time ,try again later"
                        })
               
                try:
                    
                    Following.objects.get(user=request.user ,following=user).delete()
                    Followers.objects.get(user=user, follower = request.user).delete()
                    user.followers_number -= 1
                    user.save()
                    return JsonResponse({
                        "followed":False,
                         "current_followers" :user.followers_number
                    })
                except Exception as e:
                    print(e)
                    return JsonResponse({
                            "error":"oops something happened , try again later"
                     },status=404)


            return JsonResponse({
                "error":"Can't follow yourself"
            },status=404)

        except User.DoesNotExist:
            return JsonResponse({
                "error":"could not follow user at this time"
            },status=404)

    return JsonResponse({
        "error":"request must be a PUT request"
    },status=404)

            










@csrf_protect
@login_required
def edit(request):
    if request.method == "PUT":
        request_data= json.loads(request.body)
        if not request_data.get("new_content"):
            return JsonResponse({
                "error":"no updated content recieved"
            })
        if request_data.get("new_content").isspace():
            return JsonResponse({
                "error":"no updated content recieved"
            })
           
        try:
            post_to_update = Post.objects.get(pk=request_data.get("id"))

            if not request.user == post_to_update.user:
                return JsonResponse({
                    "error":"could not update post at this time"
                })

            post_to_update.content = request_data.get("new_content")
            post_to_update.save()
            return JsonResponse({
                "updated":True,
                "new_update":post_to_update.content
            }) 
            
        except Post.DoesNotExist:
            return JsonResponse({
                "error":"could not edit post at this time"
            })
    return JsonResponse({
        "error":"request must be a PUT request"
    },status=4)
    
