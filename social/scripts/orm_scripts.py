from ..models import Post,Follow,Comment,Profile
from django.db.models import Subquery,Count

def run():

    # # post listing
    follows=Follow.objects.filter(follower=1)
    x = list(Follow.objects.values_list('following', flat=True))
    x.append(1)
    print(x)
    # ids=[]
    # for i in follows:
    #     ids.append(i.id)
    # ids.append(1)
    # posts=Post.objects.filter(user_id__in=x)
    # print(posts)
    # # post_items = Post.objects.filter(user__in=(ids)).all().order_by("-timestamp")
    # # comment=Comment.objects.filter(post_id__in=Subquery(post_items.values('pk')))
    # following = Follow.objects.filter(follower=1)
    # followed_usernames = following.values_list('following__username', flat=True)  # Get a list of followed usernames
    # post_items = Post.objects.annotate(comment_count=Count('comments')).filter(user__in=ids).all().order_by("-timestamp")
    # print(post_items) 
    # print(followed_usernames)
    # post = Post.objects.filter(user_id=1)
    # comment_count=Post.objects.annotate(count=Count('comments')).filter(user_id=1)
    # comment_count=comment_count.values_list('count', flat=True)
    # print(comment_count)
    # postu=Post.objects.all()[0]
    # profile=Profile.objects.get(id=1)

    # for post in profile.favorite.all():
    #     if postu == post:
    #         print(post)
    #     else:
    #         print('post')
