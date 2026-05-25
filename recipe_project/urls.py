from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gallery import views as gallery_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth routes (custom views)
    path('login/', gallery_views.CustomLoginView.as_view(), name='login'),
    path('logout/', gallery_views.CustomLogoutView.as_view(), name='logout'),
    path('register/', gallery_views.RegisterView.as_view(), name='register'),

    # Gallery app
    path('', include('gallery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)