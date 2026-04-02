import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Topic, ForumPost, ForumMember


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['topic_count'] = Topic.objects.count()
    ctx['topic_open'] = Topic.objects.filter(status='open').count()
    ctx['topic_closed'] = Topic.objects.filter(status='closed').count()
    ctx['topic_pinned'] = Topic.objects.filter(status='pinned').count()
    ctx['forumpost_count'] = ForumPost.objects.count()
    ctx['forumpost_published'] = ForumPost.objects.filter(status='published').count()
    ctx['forumpost_flagged'] = ForumPost.objects.filter(status='flagged').count()
    ctx['forumpost_hidden'] = ForumPost.objects.filter(status='hidden').count()
    ctx['forummember_count'] = ForumMember.objects.count()
    ctx['forummember_member'] = ForumMember.objects.filter(role='member').count()
    ctx['forummember_moderator'] = ForumMember.objects.filter(role='moderator').count()
    ctx['forummember_admin'] = ForumMember.objects.filter(role='admin').count()
    ctx['recent'] = Topic.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def topic_list(request):
    qs = Topic.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'topic_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def topic_create(request):
    if request.method == 'POST':
        obj = Topic()
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.author = request.POST.get('author', '')
        obj.replies = request.POST.get('replies') or 0
        obj.views = request.POST.get('views') or 0
        obj.status = request.POST.get('status', '')
        obj.last_reply = request.POST.get('last_reply') or None
        obj.tags = request.POST.get('tags', '')
        obj.save()
        return redirect('/topics/')
    return render(request, 'topic_form.html', {'editing': False})


@login_required
def topic_edit(request, pk):
    obj = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.author = request.POST.get('author', '')
        obj.replies = request.POST.get('replies') or 0
        obj.views = request.POST.get('views') or 0
        obj.status = request.POST.get('status', '')
        obj.last_reply = request.POST.get('last_reply') or None
        obj.tags = request.POST.get('tags', '')
        obj.save()
        return redirect('/topics/')
    return render(request, 'topic_form.html', {'record': obj, 'editing': True})


@login_required
def topic_delete(request, pk):
    obj = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/topics/')


@login_required
def forumpost_list(request):
    qs = ForumPost.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(topic_title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'forumpost_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def forumpost_create(request):
    if request.method == 'POST':
        obj = ForumPost()
        obj.topic_title = request.POST.get('topic_title', '')
        obj.author = request.POST.get('author', '')
        obj.content = request.POST.get('content', '')
        obj.date = request.POST.get('date') or None
        obj.likes = request.POST.get('likes') or 0
        obj.status = request.POST.get('status', '')
        obj.is_solution = request.POST.get('is_solution') == 'on'
        obj.save()
        return redirect('/forumposts/')
    return render(request, 'forumpost_form.html', {'editing': False})


@login_required
def forumpost_edit(request, pk):
    obj = get_object_or_404(ForumPost, pk=pk)
    if request.method == 'POST':
        obj.topic_title = request.POST.get('topic_title', '')
        obj.author = request.POST.get('author', '')
        obj.content = request.POST.get('content', '')
        obj.date = request.POST.get('date') or None
        obj.likes = request.POST.get('likes') or 0
        obj.status = request.POST.get('status', '')
        obj.is_solution = request.POST.get('is_solution') == 'on'
        obj.save()
        return redirect('/forumposts/')
    return render(request, 'forumpost_form.html', {'record': obj, 'editing': True})


@login_required
def forumpost_delete(request, pk):
    obj = get_object_or_404(ForumPost, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/forumposts/')


@login_required
def forummember_list(request):
    qs = ForumMember.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(username__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(role=status_filter)
    return render(request, 'forummember_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def forummember_create(request):
    if request.method == 'POST':
        obj = ForumMember()
        obj.username = request.POST.get('username', '')
        obj.email = request.POST.get('email', '')
        obj.join_date = request.POST.get('join_date') or None
        obj.posts = request.POST.get('posts') or 0
        obj.reputation = request.POST.get('reputation') or 0
        obj.role = request.POST.get('role', '')
        obj.bio = request.POST.get('bio', '')
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/forummembers/')
    return render(request, 'forummember_form.html', {'editing': False})


@login_required
def forummember_edit(request, pk):
    obj = get_object_or_404(ForumMember, pk=pk)
    if request.method == 'POST':
        obj.username = request.POST.get('username', '')
        obj.email = request.POST.get('email', '')
        obj.join_date = request.POST.get('join_date') or None
        obj.posts = request.POST.get('posts') or 0
        obj.reputation = request.POST.get('reputation') or 0
        obj.role = request.POST.get('role', '')
        obj.bio = request.POST.get('bio', '')
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/forummembers/')
    return render(request, 'forummember_form.html', {'record': obj, 'editing': True})


@login_required
def forummember_delete(request, pk):
    obj = get_object_or_404(ForumMember, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/forummembers/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['topic_count'] = Topic.objects.count()
    data['forumpost_count'] = ForumPost.objects.count()
    data['forummember_count'] = ForumMember.objects.count()
    return JsonResponse(data)
