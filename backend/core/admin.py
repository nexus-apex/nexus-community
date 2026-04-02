from django.contrib import admin
from .models import Topic, ForumPost, ForumMember

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "replies", "views", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "category", "author"]

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ["topic_title", "author", "date", "likes", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["topic_title", "author"]

@admin.register(ForumMember)
class ForumMemberAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "join_date", "posts", "reputation", "created_at"]
    list_filter = ["role"]
    search_fields = ["username", "email"]
