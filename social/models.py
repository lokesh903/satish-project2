from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from django.db.models import Max
from PIL import Image

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to='media/', verbose_name="Picture")
    caption = models.CharField(max_length=10000, verbose_name="Caption")
    timestamp = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.caption)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )


class like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.TextField(null=True,blank=True)
    profile_picture=models.ImageField(upload_to='media/', default='social/static/assets1/default-user.png',null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    favorite=models.ManyToManyField(Post)

    def __str__(self):
        return self.user.username
    
#image resize

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img=Image.open(self.profile_picture.path)
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    
class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.caption


class Story(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.FileField(upload_to='media/')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_user')
    reciepient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user')
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        #sender messages function
        sender_message=Message(
            user=from_user,
            sender=from_user,
            reciepient=to_user,
            body=body,
            is_read=True
        )
        sender_message.save()

        #Reciepient messages function
        reciepient_message=Message(
            user=to_user,
            sender=from_user,
            reciepient=from_user,
            body=body,
            is_read=True
        )
        reciepient_message.save()

        return sender_message
    
    def get_message(user):
        users=[]
        messages=Message.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user':User.objects.get(pk=message['reciepient']),
                'last':message['last'],
                'unread':Message.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False).count()
            })
        return users
