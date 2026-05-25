from django import forms
from .models import RecipePhoto, Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Summer Vacation 2025',
                'id': 'id_album_title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this album...',
                'id': 'id_album_description',
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'id_album_cover_image',
            }),
        }


class RecipePhotoForm(forms.ModelForm):
    class Meta:
        model = RecipePhoto
        fields = ['title', 'description', 'image', 'album']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Sunset at the Beach',
                'id': 'id_photo_title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Caption or note for this photo...',
                'id': 'id_photo_description',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'id_photo_image',
            }),
            'album': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_photo_album',
            }),
        }


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'id': 'id_reg_username',
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com (optional)',
            'id': 'id_reg_email',
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password',
            'id': 'id_reg_password1',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat your password',
            'id': 'id_reg_password2',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data