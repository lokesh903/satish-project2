from django import forms
from .models import Post,Story

class postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['image','caption']

class postedit(forms.ModelForm):
    class Meta:
        model=Post
        fields=['image','caption']

class storyform(forms.ModelForm):
    class Meta:
        model=Story
        fields=['file']