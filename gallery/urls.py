from django.urls import path
from . import views

urlpatterns = [
    # ---- Master gallery home (all photos) ----
    path('', views.GalleryHomeView.as_view(), name='gallery_home'),

    # ---- Album CRUD ----
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('albums/new/', views.AlbumCreateView.as_view(), name='album_create'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('albums/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album_update'),
    path('albums/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album_delete'),

    # ---- Photo CRUD ----
    path('photos/upload/', views.PhotoCreateView.as_view(), name='photo_create'),
    path('photos/<int:pk>/edit/', views.PhotoUpdateView.as_view(), name='photo_update'),
    path('photos/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),

    # ---- Legacy aliases (backward compatibility) ----
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
]
