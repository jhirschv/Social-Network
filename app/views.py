import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .models import User, Post, Follow, Like, Comment


def index(request):
    user = request.user
    if user.is_authenticated:
        following = Follow.objects.filter(follower=user)
        allPosts = Post.objects.all().order_by("id").reverse()
    else:
        following = None
        allPosts = Post.objects.all().order_by("id").reverse()

    page = request.GET.get('page')

    paginator = Paginator(allPosts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, "index.html", {
        "posts": posts, "following": following
        })

def direct_message(request):
    user = request.user
    if user.is_authenticated:
        following = Follow.objects.filter(follower=user)
    else:
        following = None

    return render(request, "messages.html", {
        "following": following
    })

def chat_room(request):
    user = request.user
    if user.is_authenticated:
        following = Follow.objects.filter(follower=user)
    else:
        following = None
    return render(request, "chat_room.html", {
        "following": following
    })

def profile(request, id):
    profile = User.objects.get(pk=id)

    allUserPosts = Post.objects.filter(user=id).order_by("id").reverse()

    followers = Follow.objects.filter(followed=profile)
    following = Follow.objects.filter(follower=profile)

    try:
        checkFollow = followers.filter(follower=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False


    return render(request, "profile.html", {"profile": profile, "allUserPosts": allUserPosts, "followers": followers, "following" : following, "isFollowing": isFollowing})

def profile_update(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        request.user.profile_picture = profile_picture
        request.user.save()

    return render(request, 'index.html')

def newPost(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))

def follow(request, id):
    user_to_follow = User.objects.get(pk=id)
    Follow.objects.create(follower=request.user, followed=user_to_follow)
    return redirect(reverse('profile', args=[id]))

def unfollow(request, id):
    user_to_unfollow = User.objects.get(pk=id)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect(reverse('profile', args=[id]))

@csrf_exempt
def like_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("post_id")
        post = Post.objects.get(pk=id)
        user = User.objects.get(pk=request.user.id)

        existing_like = Like.objects.filter(user=user, post=post).first()

        if existing_like:
            existing_like.delete()
        else:
            new_like = Like(user=user, post=post)
            new_like.save()

        return JsonResponse({"message": "Like state changed successfully."}, status=200)

def update_likes(request, postId):
    post = Post.objects.get(pk=postId)
    likes = post.likes.count()
    liked = Like.objects.filter(user=request.user, post=post).exists()
    return JsonResponse({"likes": likes, 'liked': liked})

@csrf_exempt
def create_comment(request, postId):
    if request.method == "POST":

        data = json.loads(request.body)
        content = data.get("comment")
        user = request.user
        post = Post.objects.get(pk=postId)
        post = Comment(
            user=user,
            post=post,
            content=content
        )
        post.save()
        return JsonResponse({"message": "Comment created successfully."}, status=201)


def update_comments(request, postId):
    post = Post.objects.get(pk=postId)
    comments = Comment.objects.filter(post=post)
    comment_count = comments.count()
    commented = Comment.objects.filter(user=request.user, post=post).exists()
    comments_list = list(comments.values('id', 'user__username', 'content', 'created_at'))
    return JsonResponse({"comments": comments_list, "comment_count": comment_count, "commented": commented})

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
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


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
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")