from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
import cloudinary.uploader

from .models import Album, RecipePhoto
from .forms import AlbumForm, RecipePhotoForm, RegisterForm


# ---------------------------------------------------------------------------
# Mixins
# ---------------------------------------------------------------------------

class AdminRequiredMixin(UserPassesTestMixin):
    """Only staff/superuser (album administrators) may pass."""
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You do not have permission to perform this action. "
            "Album management is restricted to administrators."
        )
        return redirect('gallery_home')


# ---------------------------------------------------------------------------
# Auth Views
# ---------------------------------------------------------------------------

class RegisterView(View):
    """Standard-user self-registration."""
    template_name = 'registration/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('gallery_home')
        from django.shortcuts import render
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        from django.shortcuts import render
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data.get('email', '')
            password = form.cleaned_data['password1']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
                return render(request, self.template_name, {'form': form})
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            login(request, user)
            messages.success(request, f"Welcome, {username}! Your account has been created.")
            return redirect('gallery_home')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(View):
    """Login view that works with our custom template."""
    template_name = 'registration/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('gallery_home')
        from django.shortcuts import render
        return render(request, self.template_name, {'next': request.GET.get('next', '')})

    def post(self, request):
        from django.shortcuts import render
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        next_url = request.POST.get('next', 'gallery_home')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url or 'gallery_home')
        messages.error(request, "Invalid username or password.")
        return render(request, self.template_name, {
            'next': next_url,
            'username_value': username,
        })


class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('gallery_home')

    # Allow GET for simple logout links
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('gallery_home')


# ---------------------------------------------------------------------------
# Album Views
# ---------------------------------------------------------------------------

class AlbumListView(ListView):
    """Public: anyone can browse albums."""
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'
    paginate_by = 9

    def get_queryset(self):
        qs = Album.objects.all().order_by('-created_at')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class AlbumDetailView(DetailView):
    """Public: view all photos inside an album."""
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['photos'] = self.object.photos.all()
        ctx['photo_form'] = RecipePhotoForm(initial={'album': self.object})
        return ctx


class AlbumCreateView(AdminRequiredMixin, CreateView):
    """Admin only: create a new album."""
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('gallery_home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Album '{form.instance.title}' created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class AlbumUpdateView(AdminRequiredMixin, UpdateView):
    """Admin only: update album metadata."""
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('gallery_home')

    def form_valid(self, form):
        messages.success(self.request, f"Album '{form.instance.title}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Update'
        return ctx


class AlbumDeleteView(AdminRequiredMixin, DeleteView):
    """Admin only: delete an album (photos become orphans, Cloudinary assets preserved)."""
    model = Album
    template_name = 'gallery/album_confirm_delete.html'
    success_url = reverse_lazy('gallery_home')

    def form_valid(self, form):
        messages.success(self.request, f"Album '{self.object.title}' has been deleted.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Photo (RecipePhoto) Views
# ---------------------------------------------------------------------------

class GalleryHomeView(ListView):
    """Public: master photo wall — all photos across all albums."""
    model = RecipePhoto
    template_name = 'gallery/home.html'
    context_object_name = 'photos'
    paginate_by = 12

    def get_queryset(self):
        qs = RecipePhoto.objects.all().order_by('-uploaded_at')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        ctx['albums'] = Album.objects.all().order_by('title')
        return ctx


class PhotoCreateView(LoginRequiredMixin, CreateView):
    """Authenticated users: upload a new photo."""
    model = RecipePhoto
    form_class = RecipePhotoForm
    template_name = 'gallery/photo_form.html'
    success_url = reverse_lazy('gallery_home')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Photo '{form.instance.title}' uploaded successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Upload'
        return ctx


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Owner OR admin may edit a photo."""
    model = RecipePhoto
    form_class = RecipePhotoForm
    template_name = 'gallery/photo_form.html'
    success_url = reverse_lazy('gallery_home')
    login_url = '/login/'

    def test_func(self):
        photo = self.get_object()
        user = self.request.user
        return (
            user.is_staff or
            user.is_superuser or
            photo.owner == user
        )

    def handle_no_permission(self):
        messages.error(self.request, "You can only edit your own photos.")
        return redirect('gallery_home')

    def form_valid(self, form):
        messages.success(self.request, f"Photo '{form.instance.title}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        ctx['photo'] = self.object
        return ctx


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Owner OR admin may delete a photo (also removes from Cloudinary)."""
    model = RecipePhoto
    template_name = 'gallery/delete.html'
    success_url = reverse_lazy('gallery_home')
    login_url = '/login/'

    def test_func(self):
        photo = self.get_object()
        user = self.request.user
        return (
            user.is_staff or
            user.is_superuser or
            photo.owner == user
        )

    def handle_no_permission(self):
        messages.error(self.request, "You can only delete your own photos.")
        return redirect('gallery_home')

    def form_valid(self, form):
        photo = self.get_object()
        title = photo.title
        # Remove asset from Cloudinary storage
        if photo.image:
            try:
                cloudinary.uploader.destroy(photo.image.public_id)
            except Exception as e:
                print(f"Cloudinary deletion failed: {e}")
        messages.success(self.request, f"'{title}' was permanently deleted.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['photo'] = self.object
        return ctx


# ---------------------------------------------------------------------------
# Legacy FBV aliases kept for URL backward-compatibility
# (the old urls.py referenced edit_recipe and delete_recipe)
# ---------------------------------------------------------------------------

def edit_recipe(request, pk):
    photo = get_object_or_404(RecipePhoto, pk=pk)
    if not request.user.is_authenticated:
        return redirect(f'/login/?next=/recipe/{pk}/edit/')
    if not (request.user.is_staff or request.user.is_superuser or photo.owner == request.user):
        messages.error(request, "You can only edit your own photos.")
        return redirect('gallery_home')
    view = PhotoUpdateView.as_view()
    return view(request, pk=pk)


def delete_recipe(request, pk):
    photo = get_object_or_404(RecipePhoto, pk=pk)
    if not request.user.is_authenticated:
        return redirect(f'/login/?next=/recipe/{pk}/delete/')
    if not (request.user.is_staff or request.user.is_superuser or photo.owner == request.user):
        messages.error(request, "You can only delete your own photos.")
        return redirect('gallery_home')
    view = PhotoDeleteView.as_view()
    return view(request, pk=pk)


# Keep the old gallery_view name pointing to the new CBV for existing url names
def gallery_view(request):
    view = GalleryHomeView.as_view()
    return view(request)