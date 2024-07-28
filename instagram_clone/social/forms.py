from django import forms
from .models import Post

class postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['image','caption']

class postedit(forms.ModelForm):
    class Meta:
        model=Post
        fields=['image','caption']
