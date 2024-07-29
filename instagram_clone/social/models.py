from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone



class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/')
    caption=models.CharField(max_length=50)
    timestamps = models.DateTimeField(auto_now_add=True)
    likes=models.IntegerField(default=0)


    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images', default='https://media.istockphoto.com/id/1337144146/vector/default-avatar-profile-icon-vector.jpg?s=612x612&w=0&k=20&c=BIbFwuv7FxTWvh5S3vB6bkT0Qv8Vn8N5Ffseq84ClGI=')
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(default=datetime.date.today)
    favorite=models.ManyToManyField(Post)
    # following=models.ManyToManyField(User)

    def __str__(self):
        return self.user.username



class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.CharField(max_length=1000)
    created_date=models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user.username
    
class Story(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.ImageField(upload_to='images/')
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    following=models.OneToOneField(User,on_delete=models.CASCADE,related_name='following', null=True)
    followers=models.ManyToManyField(User,related_name='followers')

    def __str__(self):
        return self.user.username