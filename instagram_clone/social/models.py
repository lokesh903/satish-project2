from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone



class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')
    image=models.ImageField(upload_to='images/')
    caption=models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes=models.IntegerField(default=0)


    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/', default='')
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(default=datetime.date.today)
    favorite=models.ManyToManyField(Post)
    following=models.ManyToManyField('self', symmetrical=False, related_name='follower',blank=True)

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
    
