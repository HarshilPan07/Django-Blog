from django.urls import path

from .views import (
        HomeView, 
        Home_Most_Liked_View,
        CreatePostView, 
        UpdatePostView, 
        DeletePostView, 
        BoardsView, 
        BoardDetailView, 
        CreateBoardView, 
        post_view, 
        like_post, 
        dislike_post, 
        like_comment,
        dislike_comment,
    )

from user.views import subscribe, unsubscribe

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('/top_all/', Home_Most_Liked_View.as_view(), name='top-all-view'),
    path('boards/', BoardsView.as_view(), name='boards'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail-list'),
    path('create-board/', CreateBoardView.as_view(), name='create-board'),
    path('boards/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('boards/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('post/<int:pk>/', post_view, name='post'),
    path('post/<int:pk>/like/', like_post, name='like-post'),
    path('post/<int:pk>/dislike/', dislike_post, name='dislike-post'),
    path('post/<int:post_pk>/like-comment/<int:comment_pk>', like_comment, name='like-comment'),
    path('post/<int:post_pk>/dislike-comment/<int:comment_pk>', dislike_comment, name='dislike-comment'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/update-post/', UpdatePostView.as_view(), name='update-post'),
    path('post/<int:pk>/delete-post/', DeletePostView.as_view(), name='delete-post'),
]
