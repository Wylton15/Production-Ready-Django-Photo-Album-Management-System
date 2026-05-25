from django.contrib import admin
from .models import RecipePhoto, Album


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'photo_count', 'created_at')
    list_filter = ('created_by',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RecipePhoto)
class RecipePhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'owner', 'uploaded_at')
    list_filter = ('album', 'owner')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at',)