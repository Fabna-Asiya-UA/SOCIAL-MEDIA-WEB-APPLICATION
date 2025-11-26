from django import forms
from .models import Addposts,Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Addposts
        fields = ['caption', 'image']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'user_photo']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
