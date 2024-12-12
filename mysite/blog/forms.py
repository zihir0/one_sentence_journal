from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = [
            'title',
            'content',
            'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 50}),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'maxlength': 280, 
                'rows': 4,
                'placeholder': 'Write your post (max 280 characters)'
            }),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'maxlength': 280, 
                'rows': 2,
                'placeholder': 'Write a comment (max 280 characters)'
            })
        }
        
class YourSignUpForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'