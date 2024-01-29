from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("profile/<int:id>", views.profile, name="profile"),
    path('follow/<int:id>', views.follow, name='follow'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),
    path('like_post/', views.like_post, name='like_post'),
    path('update_likes/<int:postId>', views.update_likes, name='update_likes'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('update_comments/<int:postId>', views.update_comments, name='update_comments'),
    path('create_comment/<int:postId>', views.create_comment, name='create_comment'),
    path('direct_message/', views.direct_message, name='direct_message'),
    path('chat_room/', views.chat_room, name="chat_room")
]