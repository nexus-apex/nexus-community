from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, default="")
    author = models.CharField(max_length=255, blank=True, default="")
    replies = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("open", "Open"), ("closed", "Closed"), ("pinned", "Pinned"), ("locked", "Locked")], default="open")
    last_reply = models.DateField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ForumPost(models.Model):
    topic_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, default="")
    content = models.TextField(blank=True, default="")
    date = models.DateField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("published", "Published"), ("flagged", "Flagged"), ("hidden", "Hidden")], default="published")
    is_solution = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.topic_title

class ForumMember(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    join_date = models.DateField(null=True, blank=True)
    posts = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    role = models.CharField(max_length=50, choices=[("member", "Member"), ("moderator", "Moderator"), ("admin", "Admin")], default="member")
    bio = models.TextField(blank=True, default="")
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.username
