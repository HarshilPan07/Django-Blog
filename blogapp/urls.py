"""blogapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from user.views import (
        Login, 
        Logout,
        register, 
        view_profile,
        profile_top_posts,
        profile_controversial_posts, 
        update_information, 
        profile_comments, 
        profile_top_comments,
        profile_controversial_comments,
        profile_likes, 
        profile_dislikes,
        user_subscriptions
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('blog.urls')),
    path('register/', register, name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('subscriptions/', user_subscriptions, name='user-subscriptions'),

    path('profile/<int:pk>/', view_profile, name='view-profile'),
    path('profile/<int:pk>/top_posts/', profile_top_posts, name='profile-top-posts'),
    path('profile/<int:pk>/controversial_posts/', profile_controversial_posts, name='profile-controversial-posts'),
    path('profile/<int:pk>/comments/', profile_comments, name='profile-comments'),
    path('profile/<int:pk>/comments/top/', profile_top_comments, name='profile-top-comments'),
    path('profile/<int:pk>/comments/controversial/', profile_controversial_comments, name='profile-controversial-comments'),
    path('profile/likes/', profile_likes, name='profile-likes'),
    path('profile/dislikes/', profile_dislikes, name='profile-dislikes'),
    path('profile/update_information/', update_information, name='update-information'),
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 