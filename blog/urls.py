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
        edit_comment,
        delete_comment,
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
    
    path('create-board/', CreateBoardView.as_view(), name='create-board'),
    path('boards/', BoardsView.as_view(), name='boards'),
    path('boards/<int:pk>/', board_detail, name='board-detail-list'),
    path('boards/<int:pk>/top_all/', board_detail_most_liked, name='board-top-all'),
    path('boards/<int:pk>/controversial/', board_detail_most_disliked, name='board-controversial'),
    path('boards/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('boards/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
    
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('boards/<int:board_pk>/post/<int:post_pk>/', post_view, name='post'),
    path('boards/<int:board_pk>/post/<int:post_pk>/comment/<int:comment_pk>/edit-comment/', edit_comment, name='edit-comment'),
    path('boards/<int:board_pk>/post/<int:post_pk>/comment/<int:comment_pk>/delete-comment/', delete_comment, name='delete-comment'),
    path('boards/<int:board_pk>/post/<int:post_pk>/top-comments/', post_view_top_comments, name='post-top-comments'),
    path('boards/<int:board_pk>/post/<int:post_pk>/controversial-comments/', post_view_controversial_comments, name='post-controversial-comments'),
    path('boards/<int:board_pk>/post/<int:post_pk>/like/', like_post, name='like-post'),
    path('boards/<int:board_pk>/post/<int:post_pk>/dislike/', dislike_post, name='dislike-post'),
    path('boards/<int:board_pk>/post/<int:post_pk>/like-comment/<int:comment_pk>', like_comment, name='like-comment'),
    path('boards/<int:board_pk>/post/<int:post_pk>/dislike-comment/<int:comment_pk>', dislike_comment, name='dislike-comment'),
    path('boards/<int:board_pk>/post/<int:pk>/update-post/', UpdatePostView.as_view(), name='update-post'),
    path('boards/<int:board_pk>/post/<int:pk>/delete-post/', DeletePostView.as_view(), name='delete-post'),
]
