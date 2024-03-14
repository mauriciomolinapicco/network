from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follower


def index(request):
    posts = Post.objects.all().order_by('timestamp').reverse()
    paginator = Paginator(posts, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    liked_posts = set()
    if user.is_authenticated:
        #Generate a list of post id's of every post that the user liked
        liked_posts = set(Like.objects.filter(user=user).values_list('post_id', flat=True))

    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'liked_posts': liked_posts
    })



@login_required
def post(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required"}, status=400)

    content = request.POST['postContent']
    user = request.user

    posts = Post.objects.all().order_by('timestamp').reverse()
    paginator = Paginator(posts, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    liked_posts = set()
    if user.is_authenticated:
        #Generate a list of post id's of every post that the user liked
        liked_posts = set(Like.objects.filter(user=user).values_list('post_id', flat=True))


    if content != "":
        post = Post(
            user=user,
            content=content
        )
        post.save()
        return render(request, "network/index.html",{
            'page_obj': page_obj,
            'liked_posts': liked_posts
        })
    else:
        return render(request, "network/index.html",{
            'page_obj': page_obj,
            'liked_posts': liked_posts
        })


def profile(request, id):

    profileUser = User.objects.get(pk=id)
    posts = Post.objects.filter(user=profileUser).order_by('timestamp').reverse()
    paginator = Paginator(posts, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    liked_posts = set()
    if user.is_authenticated:
        #Generate a list of post id's of every post that the user liked
        liked_posts = set(Like.objects.filter(user=user).values_list('post_id', flat=True))



    if request.user.is_authenticated:
        follows = Follower.objects.filter(follower=request.user, followed_user=profileUser).exists()
    else:
        follows = None

    return render(request, "network/profile.html",{
        "profileUser": profileUser,
        "posts": posts,
        "follows": follows,
        "followers": len(profileUser.followers.all()),
        "following": len(profileUser.following.all()),
        'page_obj': page_obj,
        'liked_posts': liked_posts

    })

#
#arreglar follow y unfoolow. Tiene que mandar los parametros ciertos
#
#
def follow(request, first_id, second_id):
    followerUser = User.objects.get(pk=first_id)
    followedUser = User.objects.get(pk=second_id)

    follow = Follower(
        follower = followerUser,
        followed_user = followedUser
    )
    follow.save()
    return render(request, "network/profile.html", {
        "profileUser": followedUser,
        "posts": Post.objects.filter(user=followedUser).order_by('timestamp').reverse(),
        "follows": Follower.objects.filter(follower=request.user, followed_user=followedUser).exists(),
        "followers": len(followedUser.followers.all()),
        "following": len(followedUser.following.all())
    })


#
#arreglar follow y unfoolow. Tiene que mandar los parametros ciertos
#
#
def unfollow(request, first_id, second_id):
    #if request.method == 'POST':
    followerUser = User.objects.get(pk=first_id)
    followedUser = User.objects.get(pk=second_id)

    follow = Follower.objects.filter(
        follower = followerUser,
        followed_user = followedUser
    )
    follow.delete()

    return render(request, "network/profile.html", {
        "profileUser": followedUser,
        "posts": Post.objects.filter(user=followedUser).order_by('timestamp').reverse(),
        "follows": Follower.objects.filter(follower=request.user, followed_user=followedUser).exists(),
        "followers": len(followedUser.followers.all()),
        "following": len(followedUser.following.all()),
    })


@login_required
def following(request):
    followingPeople = Follower.objects.filter(follower=request.user)
    posts = []
    for post in Post.objects.all().order_by('timestamp').reverse():
        for person in followingPeople:
            if post.user == person.followed_user:
                posts.append(post)

    paginator = Paginator(posts, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    liked_posts = set()
    if user.is_authenticated:
        #Generate a list of post id's of every post that the user liked
        liked_posts = set(Like.objects.filter(user=user).values_list('post_id', flat=True))



    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'liked_posts': liked_posts
    })



@csrf_exempt
def edit_post(request, id):
    if request.method == 'PUT':
        post = Post.objects.get(pk=id)
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data.get("content")
            post.save()
        return HttpResponse(status=204)

    '''post = Post.objects.get(pk=id)
    if request.user == post.user:
        newContent = request.POST['content']
        post.update(content=newContent)
        return JsonResponse({'succes': True})
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)'''


@csrf_exempt
def like_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        post_id = data.get('post_id')
        like = data.get('like')
        post = Post.objects.get(pk=post_id)

        if like == True:
            createLike = Like(user=user, post=post)
            createLike.save()
            return JsonResponse({'Success': True})
        else:
            Like.objects.get(user=user, post=post).delete()
            return JsonResponse({'Success': True})


    else:
        return JsonResponse({'Error':'POST method required'}, status=400)







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