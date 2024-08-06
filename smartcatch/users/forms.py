from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db.models.base import Model
from django.forms import ModelForm
from django import forms

from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'
        widgets = {
            'categorie': forms.Select(choices=User.options),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class UserProfileForm(ModelForm):
    pass

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id_ced', 'address', 'telephone', 'country']
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.helper = FormHelper(self)
    #    self.helper.form_method = 'post'
    #    self.helper.add_input(Submit('submit', 'Save'))