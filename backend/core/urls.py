from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/create/', views.topic_create, name='topic_create'),
    path('topics/<int:pk>/edit/', views.topic_edit, name='topic_edit'),
    path('topics/<int:pk>/delete/', views.topic_delete, name='topic_delete'),
    path('forumposts/', views.forumpost_list, name='forumpost_list'),
    path('forumposts/create/', views.forumpost_create, name='forumpost_create'),
    path('forumposts/<int:pk>/edit/', views.forumpost_edit, name='forumpost_edit'),
    path('forumposts/<int:pk>/delete/', views.forumpost_delete, name='forumpost_delete'),
    path('forummembers/', views.forummember_list, name='forummember_list'),
    path('forummembers/create/', views.forummember_create, name='forummember_create'),
    path('forummembers/<int:pk>/edit/', views.forummember_edit, name='forummember_edit'),
    path('forummembers/<int:pk>/delete/', views.forummember_delete, name='forummember_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
