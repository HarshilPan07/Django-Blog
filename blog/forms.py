from django.forms import ModelForm
from django import forms

from .models import Board, Post, Comment

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'description')
    
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'})
    }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'board')

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'class': 'form-control'}),
        'board': forms.Select(attrs={'class': 'form-control'})
    }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    widgets = {
        'content': forms.Textarea(attrs={'class': 'form-control', 'rows':5, 'cols':15}),
    }