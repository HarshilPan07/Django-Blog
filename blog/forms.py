from django.forms import ModelForm, Form
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

class SearchForm(Form):
    search_string = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control input-large mr-sm-2', 'placeholder': 'Search'}))
