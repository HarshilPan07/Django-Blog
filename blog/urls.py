from django.urls import path

from .views import HomeView, PostView, CreatePostView, UpdatePostView, DeletePostView, BoardsView, BoardDetailView, CreateBoardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('boards/', BoardsView.as_view(), name='boards'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail-list'),
    path('create-board/', CreateBoardView.as_view(), name='create-board'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/update-post/', UpdatePostView.as_view(), name='update-post'),
    path('post/<int:pk>/delete-post/', DeletePostView.as_view(), name='delete-post'),
]
