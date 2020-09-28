from django.urls import path

from .views import (
        HomeView, 
        Home_Most_Liked_View,
        Home_Most_Disliked_View,
        CreatePostView, 
        CreatePostInBoardView,
        UpdatePostView, 
        DeletePostView, 
        BoardsView, 
        board_detail,
        board_detail_most_liked,
        board_detail_most_disliked,
        CreateBoardView, 
        post_view, 
        post_view_top_comments,
        post_view_controversial_comments,
        like_post, 
        dislike_post, 
        like_comment,
        dislike_comment,
    )

from user.views import subscribe, unsubscribe

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('top_all/', Home_Most_Liked_View.as_view(), name='home-top-all'),
    path('controversial/', Home_Most_Disliked_View.as_view(), name='home-controversial'),
    path('boards/', BoardsView.as_view(), name='boards'),
    path('boards/<int:pk>/', board_detail, name='board-detail-list'),
    path('boards/<int:pk>/top_all/', board_detail_most_liked, name='board-top-all'),
    path('boards/<int:pk>/controversial/', board_detail_most_disliked, name='board-controversial'),
    path('create-board/', CreateBoardView.as_view(), name='create-board'),
    path('boards/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('boards/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('boards/<int:board_pk>/post/<int:pk>/', post_view, name='post'),
    path('post/<int:pk>/top-comments/', post_view_top_comments, name='post-top-comments'),
    path('post/<int:pk>/controversial-comments/', post_view_controversial_comments, name='post-controversial-comments'),
    path('post/<int:pk>/like/', like_post, name='like-post'),
    path('post/<int:pk>/dislike/', dislike_post, name='dislike-post'),
    path('post/<int:post_pk>/like-comment/<int:comment_pk>', like_comment, name='like-comment'),
    path('post/<int:post_pk>/dislike-comment/<int:comment_pk>', dislike_comment, name='dislike-comment'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/update-post/', UpdatePostView.as_view(), name='update-post'),
    path('boards/<int:board_pk>/post/<int:pk>/delete-post/', DeletePostView.as_view(), name='delete-post'),
]
