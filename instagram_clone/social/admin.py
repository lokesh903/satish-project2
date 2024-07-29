from django.contrib import admin
from .models import Profile,Post,Comment,like,Follow

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(like)
admin.site.register(Follow)

