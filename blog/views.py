from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
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

@login_required(redirect_field_name='redirect-to', login_url='login')
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if post not in user.post_likes.all() and post not in user.post_dislikes.all():  #   If Not liked or disliked
        user.post_likes.add(post)                                                   #   Like it
    elif post in user.post_likes.all():                                             #   If Liked already
        user.post_likes.remove(post)                                                #   Undo like
    elif post in user.post_dislikes.all():                                          #   If Disliked
        user.post_dislikes.remove(post)                                             #   Remove dislike and add like
        user.post_likes.add(post)

    return HttpResponseRedirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if post not in user.post_likes.all() and post not in user.post_dislikes.all():  #   If Not liked or disliked
        user.post_dislikes.add(post)                                                #   Disike it
    elif post in user.post_dislikes.all():                                          #   If Disiked already
        user.post_dislikes.remove(post)                                             #   Undo dislike
    elif post in user.post_likes.all():                                             #   If Liked
        user.post_likes.remove(post)                                                #   Remove like and add dislike
        user.post_dislikes.add(post)

    return HttpResponseRedirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def like_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    
    if comment not in user.comment_likes.all() and comment not in user.comment_dislikes.all():  #   If Not liked or disliked
        user.comment_likes.add(comment)                                                         #   Like it
    elif comment in user.comment_likes.all():                                                   #   If Liked already
        user.comment_likes.remove(comment)                                                      #   Undo like
    elif comment in user.comment_dislikes.all():                                                #   If Disliked
        user.comment_dislikes.remove(comment)                                                   #   Remove dislike and add like
        user.comment_likes.add(comment)

    return HttpResponseRedirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def dislike_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    
    if comment not in user.comment_dislikes.all() and comment not in user.comment_likes.all():  #   If Not liked or disliked
        user.comment_dislikes.add(comment)                                                         #   Like it
    elif comment in user.comment_dislikes.all():                                                   #   If Liked already
        user.comment_dislikes.remove(comment)                                                      #   Undo like
    elif comment in user.comment_likes.all():                                                #   If Disliked
        user.comment_likes.remove(comment)                                                   #   Remove dislike and add like
        user.comment_dislikes.add(comment)

    return HttpResponseRedirect(reverse('post', args=[post.id]))