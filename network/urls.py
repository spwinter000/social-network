from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path("posts/<int:post_id>", views.posts, name="posts"),
    path("posts", views.posts, name="posts"),
    path("new_post", views.new_post, name="new_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("following_page", views.following_page, name="following_page"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("profile/<int:user_id>", views.profile, name="profile")
]
