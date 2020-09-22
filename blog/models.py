from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect
from django.utils import timezone

class Board(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=2000)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("board-detail-list", kwargs={"pk": self.pk})
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(auto_now=timezone.now())
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='post_dislikes')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": self.pk})
        
class Comment(models.Model):
    content = models.CharField("Comment", max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": self.pk})


