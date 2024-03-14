from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("unfollow/<int:first_id>/<int:second_id>", views.unfollow, name="unfollow"),
    path("follow/<int:first_id>/<int:second_id>", views.follow, name="follow"),

    #API Routes
    path("/post", views.post, name="post"),
    path("editpost/<int:id>", views.edit_post, name="editpost"),
    path("likepost", views.like_post, name="likepost")
]