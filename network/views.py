from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import datetime
import json

from .models import User, UserProfile, Post, Following, Like

def index(request):
    posts = Post.objects.order_by('-timestamp').all()

    # get user profile pictures for posts
    user_profiles = UserProfile.objects.all()
    user_profile_dict = profile_pictures(user_profiles)

    # pagination
    page_obj = paginate(posts, 10, request)

    return render(request, "network/index.html", {
        "posts": posts,
        "user_profile_dict": user_profile_dict,
        'page_obj': page_obj
    })

def profile_pictures(profile_list):
    user_profile_dict = {}
    for profile in profile_list:
        user = profile.user.username
        profile_picture = profile.profile_picture.url
        user_profile_dict.update({user: profile_picture})
    return user_profile_dict

def paginate(posts_list, total_posts, request):
    paginator = Paginator(posts_list, total_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def new_post(request):
    user = request.user
    if request.method == 'POST':
        content = request.POST.get("content")
        likes = 0
        new_post = Post(user=user, content=content, timestamp=datetime)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html")

@csrf_exempt
def edit_post(request, post_id):
    data = json.loads(request.body)
    Post.objects.filter(id=post_id).update(content=data['content'])
    return HttpResponseRedirect(reverse("index"))

# for fetching post data in js
@csrf_exempt
def posts(request):
    posts = Post.objects.order_by('-timestamp').all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def profile(request, user_id):
    posts = Post.objects.order_by('-timestamp').filter(user=user_id)
    post = posts.first()
    posts_count = len(posts)

    # pagination
    page_obj = paginate(posts, 10, request)
    # page_obj_length = len(page_obj)


    # get main profile picture 
    profile = UserProfile.objects.get(user=user_id)
    profile_picture = profile.profile_picture

    # get user bio
    bio = profile.bio

    # get user profile pictures for posts
    user_profiles = UserProfile.objects.all()
    user_profile_dict = profile_pictures(user_profiles)

    # get follower and following counts
    user = User.objects.get(pk=user_id)
    followings = Following.objects.filter(follower=user)
    followings_count = len(followings)

    followers = Following.objects.filter(followed=user)
    followers_count = len(followers)

    # check to see if request.user is following current user 
    following = Following.objects.filter(follower=request.user, followed=user_id, following=True)
    if following.exists():
        user_follows = True
    else:
        user_follows = False

    following_back = Following.objects.filter(follower=user_id, followed=request.user, following=True)

    path = request.path
    return render(request, "network/profile.html", {
        "posts": posts,
        "post": post,
        "profile_picture": profile_picture,
        "bio": bio,
        "user_profile_dict": user_profile_dict,
        "user": user, 
        "posts_count": posts_count,
        "followings_count": followings_count,
        "followers_count": followers_count,
        "following": following,
        "user_follows": user_follows,
        "following_back": following_back,
        "page_obj": page_obj
    })

def follow(request, user_id):
    user = User.objects.get(pk=user_id)
    follower = request.user
    followed = User.objects.get(pk=user_id)
    if request.method == 'POST':
        new_follow = Following(follower=follower, followed=followed, following=True)
        new_follow.save()
        return HttpResponseRedirect(reverse("profile", args=(user.id, )))
    return render(request, "network/index.html")

def unfollow(request, user_id):
    user = User.objects.get(pk=user_id)
    unfollow = Following.objects.filter(follower=request.user, followed=user_id, following=True).delete()
    return HttpResponseRedirect(reverse("profile", args=(user.id, )))  

def following_page(request):
    # get a list of users that request.user is 'following'
    list_of_following = Following.objects.filter(follower=request.user)
    following_list = [user.followed for user in list_of_following]
    message = ""
    if len(following_list) == 0:
        message = "You aren't following anyone yet!"
    # get list of posts by users in the following_list, then take list of objects and put them into new list to be sorted...
    post_list = []
    for user in following_list:   
        posts = Post.objects.filter(user=user)
        post_list.append(posts)
    new_post_list = []
    for post_object in post_list:
        for post in post_object:
            new_post_list.append(post)
            new_post_list.sort(key=lambda x: x.timestamp, reverse=True)

    # pagination
    page_obj = paginate(new_post_list, 10, request)

    # get profile pictures for posts
    user_profiles = UserProfile.objects.all()
    user_profile_dict = profile_pictures(user_profiles)

    return render(request, "network/following_page.html", {
        "following_list": following_list,
        "message": message,
        "page_obj": page_obj,
        "user_profile_dict": user_profile_dict
    })

@csrf_exempt
def like(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    check_for_like = Like.objects.filter(user=user, post=post)
    # check if post has been liked, if so delete like item from db and subtract one like from post object
    if check_for_like.exists():
        check_for_like = check_for_like.delete()

        post = post.likes.remove(user)
    else:
        new_like = Like(liked=True)
        new_like.save()
        new_like.user.add(user)
        new_like.post.add(post)

        post = post.likes.add(user)
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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        profile_picture = request.FILES["pro_pic"] #image data is only accessible this way
        # what about the user bio? Not good for registration page

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
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            profile = UserProfile.objects.create(user=user, profile_picture=profile_picture)
            profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
