
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post",views.new_post,name="new_post"),
    path("all_post/<int:page_num>",views.all_post,name="all_post"),

    #APi routes
    path("edit_post",views.edit_post,name="edit_post"),
    path("favourite",views.like_or_unlike,name="like_or_unlike")
]
