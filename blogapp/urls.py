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
        update_information, 
        profile_comments, 
        profile_likes, 
        profile_dislikes,
        user_subscriptions
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('profile/<int:pk>/', view_profile, name='view-profile'),
    path('profile/<int:pk>/comments/', profile_comments, name='profile-comments'),
    path('profile/<int:pk>/likes/', profile_likes, name='profile-likes'),
    path('profile/<int:pk>/dislikes/', profile_dislikes, name='profile-dislikes'),
    path('profile/<int:pk>/update_information/', update_information, name='update-information'),
    path('subscriptions/', user_subscriptions, name='user-subscriptions'),
    path('register/', register, name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 