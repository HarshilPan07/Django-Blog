from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from blog.models import Board, Post

LOGIN_URL = 'login'
REIDRECT_FIELD_NAME = 'next='

def register(request):
    """
    Uses CreateUserForm(), fields=(username, email, password1, password2)
    Checks if valid and saves form if POST, sends empty else 
    """

    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)

        if register_form.is_valid():
            register_form.save()
        
            return redirect('login')
    else:
        register_form = CreateUserForm()
        context = {'register_form': register_form}
        
    return render(request, 'blog/register.html', context)

class Login(LoginView):
    template_name = 'blog/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    login_url = 'login'
    redirect_field_name = 'redirect-to'
    template_name = 'blog/logout.html'
    
def view_profile(request, pk):
    """
    Gets User instance of profile's user using pk
    Gets list of Post objects and renders to profile.html
    """
    
    profile_user = get_object_or_404(User, pk=pk)
    
    post_list = list(Post.objects.filter(author=profile_user).order_by('-date_posted'))
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    context = {
        'profile_user': profile_user,
        'page_obj': page_obj, 
        }

    return render(request, 'blog/profile.html', context)

def profile_comments(request, pk):
    """
    Gets User instance of profile's user using pk
    Gets list of Comment objects and renders to profile.html
    """

    profile_user = get_object_or_404(User, pk=pk)

    paginator = Paginator(profile_user.comment_set.all(), 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile_user': profile_user,
        'page_obj': page_obj
    }

    return render(request, 'blog/profile_comments.html', context)

@login_required(redirect_field_name=REIDRECT_FIELD_NAME, login_url=LOGIN_URL)
def profile_likes(request):
    """
    Gets list of likes from request.user and renders to profile.html
    """

    paginator = Paginator(request.user.post_likes.all(), 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'blog/profile_likes.html', context)

@login_required(redirect_field_name=REIDRECT_FIELD_NAME, login_url=LOGIN_URL)
def profile_dislikes(request):
    """
    Gets list of dislikes from request.user and renders to profile.html
    """

    paginator = Paginator(request.user.post_dislikes.all(), 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'blog/profile_dislikes.html', context)

@login_required(redirect_field_name=REIDRECT_FIELD_NAME, login_url=LOGIN_URL)
def update_information(request):
    """
    Uses UserUpdateForm(), fields=(username, email) and ProfileUpdateForm(), fields=(description, picture)
    Validates and saves UserUpdateForm and ProfileUpdateForm if POST request, passes empty else
    Renders object lists and forms to profile.html with above data
    """
    
    user_update_form = UserUpdateForm(instance=request.user)
    profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
        
            return redirect('view-profile', pk=request.user.pk)
        
    context = {
        'user_update_form': user_update_form, 
        'profile_update_form': profile_update_form, 
    }

    return render(request, 'blog/profile_update_info.html', context)

@login_required(redirect_field_name=REIDRECT_FIELD_NAME, login_url=LOGIN_URL)
def user_subscriptions(request):
    subbed_boards = request.user.subs.all()

    context = {
        'subbed_boards': subbed_boards
    }
    return render(request, 'blog/subscriptions.html', context)

@login_required(redirect_field_name=REIDRECT_FIELD_NAME, login_url=LOGIN_URL)
def subscribe(request, pk):
    board = get_object_or_404(Board, pk=pk)

    board.subscription.add(request.user)

    return redirect(reverse('board-detail-list', args=[board.pk]))

@login_required(redirect_field_name=REIDRECT_FIELD_NAME, login_url=LOGIN_URL)
def unsubscribe(request, pk):
    board = get_object_or_404(Board, pk=pk)

    board.subscription.remove(request.user)

    return redirect(reverse('board-detail-list', args=[board.pk]))