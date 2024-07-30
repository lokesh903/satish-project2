from django.urls import path
from .import views
from django.contrib.auth import views as auth_views  


urlpatterns = [
    path('',views.Registration,name='Registration'),
    path('home',views.home,name='home'),
    path('Login',views.Login,name="Login"),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('Editprofile',views.Editprofile,name='Editprofile'),
    path('createpost', views.createpost,name='createpost'),
    path('editpost/<int:post_id>/',views.editpost,name='editpost'),
    path('likeview/<int:post_id>', views.likeview,name='likeview'),
    path('favorite/<int:post_id>', views.favorite,name='favorite'),
    path('deletepost/<int:post_id>', views.deletepost,name='deletepost'),
    path('addcomment/<int:post_id>/',views.addcomment,name='addcomment'),
    path('addstory',views.addstory,name='addstory'),
    path('viewstory/<int:str_id>',views.viewstory,name='viewstory'),
    path('favoritepostlist',views.favoritepostlist,name='favoritepostlist'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('following_users',views.following_users,name='following_users'),
    path('follower_list',views.follower_list,name='follower_list'),
    path('follow_user/<int:user_id>',views.follow_user,name='follow_user'),


]
