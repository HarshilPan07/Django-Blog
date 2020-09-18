from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def register(request):
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

@login_required(redirect_field_name='redirect-to', login_url='login')
def profile(request):
    post_list = request.user.post_set.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()

            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'user_update_form': user_update_form, 'profile_update_form': profile_update_form, 'page_obj': page_obj}

    return render(request, 'blog/profile.html', context)