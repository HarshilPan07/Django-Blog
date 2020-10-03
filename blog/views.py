from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .models import Board, Post, Comment
from .forms import BoardForm, PostForm, CommentForm, SearchForm

class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_boards"] = sorted(Board.objects.all(), key=lambda obj: -obj.get_popularity_rating())[:4]

        return context

def search_posts(request):
    popular_boards = sorted(Board.objects.all(), key=lambda obj: -obj.get_popularity_rating())[:4]
    
    if request.method == 'POST':    
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            search_string = search_form.cleaned_data['search_string']
            posts = Post.objects.filter(Q(title__icontains=search_string) | Q(content__icontains=search_string))
            
            paginator = Paginator(posts, 50)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

    context = {'popular_boards': popular_boards, 'search_string': search_string, 'posts': posts, 'page_obj': page_obj}

    return render(request, 'blog/search_results.html', context)

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

    def get_queryset(self):
        return Board.objects.all().order_by('title')
    
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

class CreatePostInBoardView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'content']

    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.board = Board.objects.get(pk=self.kwargs['board_pk'])

        return super().form_valid(form)

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    fields=['title', 'content']
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

def post_view(request, board_pk, post_pk):    
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.get_recent_comments()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            return redirect(reverse('post', args=[post.board.id, post.id]))
        
    else:
        comment_form = CommentForm()
    
    context = {'post': post, 'comments': comments, 'comment_form': comment_form}

    return render(request, 'blog/detail.html', context)

def edit_comment(request, board_pk, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.get_recent_comments()
    
    comment_to_edit = post.comment_set.all().get(pk=comment_pk)
    edit_comment_form = CommentForm(instance=comment_to_edit)
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'add-comment-form' in request.POST:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                
                return redirect(reverse('post', args=[post.board.id, post.id]))
        else:    
            edit_comment_form = CommentForm(request.POST, instance=comment_to_edit)

            if edit_comment_form.is_valid():
                comment_to_edit = edit_comment_form.save(commit=False)
                comment_to_edit.date_edited = timezone.now()
                comment_to_edit.save()

                return redirect(reverse('post', args=[board_pk, post_pk]))
    
    context = {'post': post, 'comments': comments, 'edit_comment_form': edit_comment_form, 'comment_form': comment_form, 'comment_to_edit': comment_to_edit}

    return render(request, 'blog/detail.html', context)

def delete_comment(request, board_pk, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.get_recent_comments()
    
    comment_to_delete = post.comment_set.all().get(pk=comment_pk)
    comment_to_delete.delete()

    context = {'post': post, 'comments': comments}
    
    return redirect(reverse('post', args=[board_pk, post_pk]))
    
def post_view_top_comments(request, board_pk, post_pk):    
    post = get_object_or_404(Post, pk=post_pk)
    comments = sorted(post.comment_set.all(), key=lambda obj: -obj.get_rating())

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            return redirect(reverse('post', args=[post.board.id, post.id]))
        
    else:
        comment_form = CommentForm()
    
    context = {'post': post, 'comments': comments, 'comment_form': comment_form}

    return render(request, 'blog/detail.html', context)

def post_view_controversial_comments(request, board_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = sorted(post.comment_set.all(), key=lambda obj: obj.get_rating())

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect(reverse('post', args=[post.board.id, post.id]))
        
    else:
        comment_form = CommentForm()
    
    context = {'post': post, 'comments': comments, 'comment_form': comment_form}

    return render(request, 'blog/detail.html', context)

@login_required
def like_post(request, board_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    
    if post not in user.post_likes.all() and post not in user.post_dislikes.all():  
        user.post_likes.add(post)                                                   
    elif post in user.post_likes.all():                                             
        user.post_likes.remove(post)                                                
    elif post in user.post_dislikes.all():                                          
        user.post_dislikes.remove(post)                                             
        user.post_likes.add(post)

    return redirect(reverse('post', args=[post.board.id, post.id]))

@login_required
def dislike_post(request, board_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    
    if post not in user.post_likes.all() and post not in user.post_dislikes.all():  
        user.post_dislikes.add(post)                                                
    elif post in user.post_dislikes.all():                                          
        user.post_dislikes.remove(post)                                             
    elif post in user.post_likes.all():                                             
        user.post_likes.remove(post)                                                
        user.post_dislikes.add(post)

    return redirect(reverse('post', args=[post.board.id, post.id]))

@login_required
def like_comment(request, board_pk, post_pk, comment_pk):    
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

    return redirect(reverse('post', args=[post.board.id, post.id]))

@login_required
def dislike_comment(request, board_pk, post_pk, comment_pk):
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

    return redirect(reverse('post', args=[post.board.id, post.id]))