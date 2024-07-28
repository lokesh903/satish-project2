from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import Profile,Post,Comment
from django.contrib.auth.decorators import login_required
from .forms import postform,postedit




def Registration(req):
    if req.method=='POST':
        first_name=req.POST.get('first_name')
        last_name=req.POST.get('last_name')
        username=req.POST.get('username')
        email=req.POST.get('email')
        password=req.POST.get('password')

        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        return redirect('Login')
    else:
        return render(req,'Registeration.html')

def Login(req):
    if req.method=='POST':
        username=req.POST.get('username')
        password=req.POST.get('password')

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(req,user)
            return redirect('home')
        else:
            messages.error(req,'Invalid Credential')
            return redirect('Login')
    else:
        return render(req,'Login.html')
    
def logout(req):
    auth.logout(req)
    return redirect('/')

def profile(req):
    user=req.user
    try:
        profile=Profile.objects.get(user=user)
        posts=Post.objects.filter(user__username=user.username)
        postcount=posts.count
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    return render(req,'Profile.html',{'profile':profile,'posts':posts,'postcount':postcount})

@login_required
def Editprofile(req):
    user=req.user
    try:
       profile=Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if req.method == 'POST':
        profile.bio = req.POST.get('bio')
        profile.profile_picture = req.FILES.get('profile_picture')
        profile.save()
        return redirect('profile')
    return render(req, 'Editprofile.html',{'profile': profile})

def home(req):
    posts=Post.objects.all()
    return render(req,'home.html',{'posts':posts})


def createpost(req):
    if req.method=='POST':
        form=postform(req.POST,req.FILES)
        if form.is_valid():
            Post=form.save(commit=False)
            Post.user=req.user
            Post.save()
            messages.success(req,'Post Created Successfully')
            return redirect('home')
        else:
            messages.error(req,'Invalid form data')
            return render(req,'postform.html',{'form':form})
    else:
        form=postform()
        return render(req,'postform.html',{'form':form})

def deletepost(req,post_id):
    post=Post.objects.get(id=post_id)
    post.delete()
    messages.success(req,'Deleted Successfully')
    return redirect('home')

def editpost(req,post_id):
    post=Post.objects.get(id=post_id)
    if req.method=='POST':
       form=postedit(req.POST,req.FILES,instance=post)
       if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=postedit(instance=post)

    return render(req,'editpost.html',{'form':form ,'post':post})

@login_required
def addcomment(req, post_id):
    if req.method == 'POST':
        post = Post.objects.get(id=post_id)
        text = req.POST.get('text')
        if text:
            comment = Comment.objects.create(
                post=post,
                user=req.user,
                text=text
            )
            comment.save()
            return redirect('home')
    return render(req, 'home.html', {'post_id': post_id})
    