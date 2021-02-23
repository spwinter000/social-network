from django.contrib import admin
from .models import User, UserProfile, Post, Following, Like

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_picture")

class LikeAdmin(admin.ModelAdmin):
    # list_display = ("user", "post")
     filter_horizontal = ("user", "post",)

class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "timestamp")
    filter_horizontal = ("likes",)

class FollowingAdmin(admin.ModelAdmin):
    list_display = ("follower", "followed", "following")

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Following, FollowingAdmin)