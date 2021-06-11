from django import forms
from django.forms import ModelForm 
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UploadPicForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone','profile_pic']


    