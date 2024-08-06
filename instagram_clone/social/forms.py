from django import forms
from .models import Post,Story,Profile
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

    def clean_firstname(self):
        firstname=self.cleaned_data.get('first_name')
        if not firstname:
            raise forms.ValidationError("Firstname is required")
        return firstname
        
    def clean_lastname(self):
        lastname=self.cleaned_data.get('last_name')
        if not lastname:
            raise forms.ValidationError("lastname is required")
        return lastname
        
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("email is required")
        return email
    
class EditProfile(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['bio','profile_picture']
    
    def clean_bio(self):
        bio=self.cleaned_data.get('bio')
        if not bio:
            raise forms.ValidationError('field required')
        return bio

    def clean_profile(self):
        profile_picture=self.cleaned_data.get('profile_picture')
        if not profile_picture:
            raise forms.ValidationError('field required')
        return profile_picture

class postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['image','caption']
    
    def clean_image(self):
        image=self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('Fields Required')
        return image

    def clean_caption(self):
        caption=self.cleaned_data.get('caption')
        if not caption:
            raise forms.ValidationError("caption Required")
        return caption
    
class postedit(forms.ModelForm):
    class Meta:
        model=Post
        fields=['image','caption']

    def clean_image(self):
        image=self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('Fields Required')
        return image

    def clean_caption(self):
        caption=self.cleaned_data.get('caption')
        if not caption:
            raise forms.ValidationError("caption Required")
        return caption

class storyform(forms.ModelForm):
    class Meta:
        model=Story
        fields=['file']
    
    def clean_file(self):
        file=self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError('field required')
        return file