from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .models import Board, Post, Comment
from .forms import BoardForm, PostForm, CommentForm

class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class BoardsView(ListView):
    model = Board
    template_name = 'blog/board_list.html'
    context_object_name = 'boards'

class BoardDetailView(DetailView):
    model = Board
    template_name = 'blog/board_post_list.html'

class CreateBoardView(LoginRequiredMixin, CreateView):
    model = Board
    template_name = 'blog/create_board.html'
    form_class = BoardForm

    login_url = 'login'
    redirect_field_name = 'redirect-to'

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = PostForm
    
    login_url = 'login'
    redirect_field_name = 'redirect-to'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    form_class = PostForm
    login_url = 'login'
    redirect_field_name = 'redirect-to'

    def test_func(self):
        post = self.get_object()
        
        if self.request.user == post.author:
            return True
        return False

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    login_url = 'login'
    redirect_field_name = 'redirect-to'
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

@login_required(redirect_field_name='redirect-to', login_url='login')
def post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.commenter = request.user
            comment.save()
        
    else:
        comment_form = CommentForm()
    
    context = {'post': post, 'comment_form': comment_form}

    return render(request, 'blog/detail.html', context)

