from django.contrib import admin
from .models import Post, Follow, Profile, Comment, Story,Message

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(Message)