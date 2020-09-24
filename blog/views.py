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
    """
    Uses CommentForm(), fields=['content']
    Gets Post object with pk
    Checks validation and saves if POST method, sends empty CommentForm() instance else
    Renders detail.html with Post object and CommentForm instance passed as context 
    """
    
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
    """
    Gets Post and User instance with pk
    Appropriately adds or removes like to post_likes/post_dislikes based whether post is liked, disliked, or none
    Returns HTTPResponseRedirect to post page with args=(post.id)
    """
    
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if post not in user.post_likes.all() and post not in user.post_dislikes.all():  
        user.post_likes.add(post)                                                   
    elif post in user.post_likes.all():                                             
        user.post_likes.remove(post)                                                
    elif post in user.post_dislikes.all():                                          
        user.post_dislikes.remove(post)                                             
        user.post_likes.add(post)

    return HttpResponseRedirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def dislike_post(request, pk):
    """
    Gets Post and User instance with pk
    Appropriately adds or removes dislike to post_likes/post_dislikes based whether post is liked, disliked, or none
    Returns HTTPResponseRedirect to post page with args=(post.id)
    """
    
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if post not in user.post_likes.all() and post not in user.post_dislikes.all():  
        user.post_dislikes.add(post)                                                
    elif post in user.post_dislikes.all():                                          
        user.post_dislikes.remove(post)                                             
    elif post in user.post_likes.all():                                             
        user.post_likes.remove(post)                                                
        user.post_dislikes.add(post)

    return HttpResponseRedirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def like_comment(request, post_pk, comment_pk):
    """
    Gets Post, User, and Comment instance with post and comment pks
    Appropriately adds or removes dislike to comment_likes/comment_dislikes based whether post is liked, disliked, or none
    Returns HTTPResponseRedirect to post page with args=(post.id)
    """
    
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    
    if comment not in user.comment_likes.all() and comment not in user.comment_dislikes.all():  
        user.comment_likes.add(comment)                                                         
    elif comment in user.comment_likes.all():                                                   
        user.comment_likes.remove(comment)                                                      
    elif comment in user.comment_dislikes.all():                                                
        user.comment_dislikes.remove(comment)                                                   
        user.comment_likes.add(comment)

    return HttpResponseRedirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def dislike_comment(request, post_pk, comment_pk):
    """
    Gets Post, User, and Comment instance with post and comment pks
    Appropriately adds or removes dislike to comment_likes/comment_dislikes based whether post is liked, disliked, or none
    Returns HTTPResponseRedirect to post page with args=(post.id)
    """
    
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    
    if comment not in user.comment_dislikes.all() and comment not in user.comment_likes.all():     
        user.comment_dislikes.add(comment)                                                         
    elif comment in user.comment_dislikes.all():                                                   
        user.comment_dislikes.remove(comment)                                                      
    elif comment in user.comment_likes.all():                                                      
        user.comment_likes.remove(comment)                                                         
        user.comment_dislikes.add(comment)

    return HttpResponseRedirect(reverse('post', args=[post.id]))