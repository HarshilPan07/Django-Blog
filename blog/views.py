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
    paginate_by = 50

class Home_Most_Liked_View(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 50

    def get_queryset(self):
        return sorted(Post.objects.all(), key=lambda obj: -obj.get_rating())

class Home_Most_Disliked_View(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 50

    def get_queryset(self):
        return sorted(Post.objects.all(), key=lambda obj: obj.get_rating())
    
class BoardsView(ListView):
    model = Board
    template_name = 'blog/board_list.html'
    context_object_name = 'boards'

def board_detail(request, pk):
    board_posts = Board.objects.get(pk=pk).post_set.all().order_by('-date_posted')
    context = {'board': Board.objects.get(pk=pk), 'board_posts': board_posts}

    return render(request, 'blog/board_post_list.html', context)

def board_detail_most_liked(request, pk):
    board_posts = sorted(Board.objects.get(pk=pk).post_set.all(), key=lambda obj: -obj.get_rating())    
    context = {'board': Board.objects.get(pk=pk), 'board_posts': board_posts}

    return render(request, 'blog/board_post_list.html', context)

def board_detail_most_disliked(request, pk):
    board_posts = sorted(Board.objects.get(pk=pk).post_set.all(), key=lambda obj: obj.get_rating())    
    context = {'board': Board.objects.get(pk=pk), 'board_posts': board_posts}

    return render(request, 'blog/board_post_list.html', context)

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

def post_view(request, pk):    
    post = get_object_or_404(Post, pk=pk)
    comments = post.get_recent_comments()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            return redirect(reverse('post', args=[post.id]))
        
    else:
        comment_form = CommentForm()
    
    context = {'post': post, 'comments': comments, 'comment_form': comment_form}

    return render(request, 'blog/detail.html', context)

def post_view_top_comments(request, pk):    
    post = get_object_or_404(Post, pk=pk)
    comments = sorted(post.comment_set.all(), key=lambda obj: -obj.get_rating())

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            return redirect(reverse('post', args=[post.id]))
        
    else:
        comment_form = CommentForm()
    
    context = {'post': post, 'comments': comments, 'comment_form': comment_form}

    return render(request, 'blog/detail.html', context)

def post_view_controversial_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = sorted(post.comment_set.all(), key=lambda obj: obj.get_rating())

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect(reverse('post', args=[post.id]))
        
    else:
        comment_form = CommentForm()
    
    context = {'post': post, 'comments': comments, 'comment_form': comment_form}

    return render(request, 'blog/detail.html', context)

@login_required(redirect_field_name='redirect-to', login_url='login')
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if post not in user.post_likes.all() and post not in user.post_dislikes.all():  
        user.post_likes.add(post)                                                   
    elif post in user.post_likes.all():                                             
        user.post_likes.remove(post)                                                
    elif post in user.post_dislikes.all():                                          
        user.post_dislikes.remove(post)                                             
        user.post_likes.add(post)

    return redirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if post not in user.post_likes.all() and post not in user.post_dislikes.all():  
        user.post_dislikes.add(post)                                                
    elif post in user.post_dislikes.all():                                          
        user.post_dislikes.remove(post)                                             
    elif post in user.post_likes.all():                                             
        user.post_likes.remove(post)                                                
        user.post_dislikes.add(post)

    return redirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def like_comment(request, post_pk, comment_pk):    
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

    return redirect(reverse('post', args=[post.id]))

@login_required(redirect_field_name='redirect-to', login_url='login')
def dislike_comment(request, post_pk, comment_pk):
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

    return redirect(reverse('post', args=[post.id]))