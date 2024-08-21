from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.Registration, name="Registration"),
    path("login/", views.login, name="login"),
    path('logout/',views.logout,name='logout'),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("index/", views.index, name="index"),
    path("newpost/", views.NewPost, name="newpost"),
    path("postdetail/<uuid:post_id>", views.postDetail, name="postdetail"),
    path('editpost/<uuid:post_id>/',views.editpost,name='editpost'),
    path('favorite/<uuid:post_id>', views.favorite,name='favorite'),
    path("likeview/<uuid:post_id>", views.likeview, name="likeview"),
    path("comment/<uuid:post_id>", views.comment, name="comment"),
    path("profile/<username>", views.UserProfile, name="profile"),
    path('Editprofile',views.Editprofile,name='Editprofile'),
    path("follow/<username>", views.follow, name="follow"),
    path('addstory/',views.addstory,name='addstory'),
    path('archive/',views.archive,name='archive'),
    path('inbox/',views.inbox,name='inbox'),
    path('direct/<username>',views.Directs,name='direct'),
    path('sendmessage/',views.SendMessage, name='sendmessage'),
    path('searchuser/',views.UserSearch, name='searchuser'),
    path('newmessage/<username>',views.NewMessage, name='newmessage'),
]
