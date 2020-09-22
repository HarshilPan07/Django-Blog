from django.forms import ModelForm
from django import forms

from .models import Board, Post, Comment

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'description')

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'board')
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    widgets = {
        'content': forms.TextInput(attrs={'class': 'form-control'}),
    }

