from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title', 'content')





class RegistrationForm(forms.Form):
    username=forms.CharField(max_length=50)
    email=forms.EmailField()