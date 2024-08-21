from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Follow, Post, like, Profile, Comment, Story, Message
from django.contrib.auth.models import User
from django.urls import resolve
from .forms import (
    NewPostform,
    CommentForm,
    RegistrationForm,
    EditProfile,
    storyform,
    postedit,
)
from django.contrib import messages
from django.contrib import auth
from django.core.paginator import Paginator
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def Registration(req):
    if req.method == "POST":
        form = RegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, "Successfully Registered")
            return redirect("login")
        else:
            messages.error(req, "All fields are required")
    else:
        form = RegistrationForm()
    return render(req, "Registration.html", {"form": form})


def login(req):
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(req, user)
            return redirect("../index/")
        else:
            messages.error(req, "Invalid Credential")
            return redirect("../login/")
    else:
        return render(req, "Login.html")


def logout(req):
    auth.logout(req)
    return redirect("/login")


def index(request):
    user = request.user
    follow_status = Follow.objects.filter(follower=user)
    followed_usernames = follow_status.values_list("following__username", flat=True)
    # Get a list of followed usernames
    x = list(Follow.objects.values_list("following", flat=True).filter(follower=user))
    x.append(user.id)
    mainProfile, create = Profile.objects.get_or_create(user=user)
    profiles = Profile.objects.exclude(user=user)
    post_items = (
        Post.objects.filter(user_id__in=x)
        .annotate(comment_count=Count("comments"))
        .all()
        .order_by("-timestamp")
    )
    id = request.user.id
    time = timezone.now() - timedelta(hours=24)

    stories = Story.objects.filter(created_at__gte=time, user_id__in=x)
    # comment=Comment.objects.filter(pk=Subquery(post_items.values('pk')))
    return render(
        request,
        "index.html",
        {
            "post_items": post_items,
            "profiles": profiles,
            "mainProfile": mainProfile,
            "followed_usernames": followed_usernames,
            "stories": stories,
        },
    )


def NewPost(request):
    user = request.user
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            Post = form.save(commit=False)
            Post.user = user
            Post.save()
            messages.success(request, "Post Created Successfully")
            return redirect("index")
    else:
        form = NewPostform()
    return render(request, "newpost.html", {"form": form})


def postDetail(request, post_id):
    post = Post.objects.prefetch_related("comments").get(id=post_id)
    context = {
        "post": post,
    }
    return render(request, "test.html", context)


def editpost(request, post_id):
    post = Post.objects.get(id=post_id, user=request.user)
    if request.method == "POST":
        form = postedit(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = postedit(instance=post)
    return render(request, "editpost.html", {"form": form, "post": post})


def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    if profile.favorite.filter(id=post_id).exists():
        profile.favorite.remove(post)
    else:
        profile.favorite.add(post)
        messages.success(request, "Added in favorite")
    return redirect("index")


def likeview(req, post_id):
    user = req.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = like.objects.filter(user=user, post=post).count()
    if not liked:
        liked = like.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = like.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
    post.likes = current_likes
    post.save()
    return redirect("../index/")


def UserProfile(req, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(req.path).url_name
    if url_name == "profile":
        posts = (
            Post.objects.prefetch_related("comments")
            .annotate(count=Count("comments"))
            .filter(user=user)
            .order_by("-timestamp")
        )
    else:
        posts.favarite.all()

    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    follower_count = Follow.objects.filter(following=user).count()
    # follow status
    follow_status = Follow.objects.filter(following=user, follower=req.user).exists()
    paginator = Paginator(posts, 3)
    page_number = req.GET.get("page")
    posts_paginator = paginator.get_page(page_number)

    context = {
        "posts_paginator": posts_paginator,
        "profile": profile,
        "posts": posts,
        "post_count": post_count,
        "following_count": following_count,
        "follower_count": follower_count,
        "follow_status": follow_status,
    }
    return render(req, "profile.html", context)


def Editprofile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = EditProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return redirect("index")
        else:
            messages.error(request, "All fields required")
    else:
        form = EditProfile(instance=profile)
    return render(request, "editprofile.html", {"form": form, "profile": profile})


def follow(req, username):
    user = req.user
    following = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(follower=user, following=following)
    if not created:
        follow.delete()
    return redirect("../index/")


# def comment(request, post_id):
#     post=Post.objects.get(id=post_id)
#     user=request.user
#     if request.method=="POST":
#         form=CommentForm(request.POST)
#         if form.is_valid():
#             comment=form.save(commit=False)
#             comment.post=post
#             comment.user=user
#             comment.save()
#             return redirect ('../index/')
#     else:
#         form=CommentForm()
#     return render(request,'index.html',{'form':form})


def comment(req, post_id):

    if req.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = req.POST.get("comment")
        if comment:
            Comment.objects.create(post=post, user=req.user, comment=comment)
            return redirect("index")
        else:
            messages.error(req, "Enter Comment")
            return redirect("index")


def addstory(request):
    user = request.user
    if request.method == "POST":
        form = storyform(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = user
            story.save()
            messages.success(request, "Story added successfully")
            return redirect("index")
    else:
        form = storyform()
    return render(request, "story.html", {"form": form})


def archive(request):
    time = timezone.now() - timedelta(hours=24)
    archive = Story.objects.filter(created_at__lte=time, user=request.user)
    return render(request, "archive.html", {"archive": archive})


@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = messages[0]["user"].username
        directs = Message.objects.filter(user=user, reciepient=messages[0]["user"])
        directs.update(is_read=True)

        for message in messages:
            if message["user"].username == active_direct:
                message["unread"] = 0

    context = {
        "directs": directs,
        "active_direct": active_direct,
        "messages": messages,
    }

    return render(request, "inbox.html", context)


def Directs(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message["user"].username == username:
            message["unread"] = 0

    context = {
        "directs": directs,
        "active_direct": active_direct,
        "messages": messages,
    }
    return render(request, "direct.html", context)


def SendMessage(request):
    from_user=request.user
    to_user_username= request.POST.get('to_user')
    body=request.POST.get('body')

    if request.method=='POST':
        to_user=User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user,body)
        return redirect('inbox')
    else:
        pass

def UserSearch(request):
    query=request.GET.get('q')
    context={}
    if query:
        users=User.objects.filter(Q(username__icontains=query))
        paginate=Paginator(users,5)
        page_number=request.GET.get('page')
        user_paginator=paginate.get_page(page_number)

        context = {
        "users": user_paginator,
        }
    return render(request, 'search.html', context)

def NewMessage(request,username):
    from_user = request.user
    body="hii"
    try:
        to_user=User.objects.get(username=username)
    except Exception as e:
        return redirect('searchuser')
    if from_user != to_user:
        Message.send_message(from_user,to_user,body)
        return redirect('inbox')