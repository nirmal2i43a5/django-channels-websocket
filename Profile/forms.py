from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


class LoginForm(AuthenticationForm):
    	# email = EmailField(label=_("Email"), required=True,help_text=_("Required.")) #Email address is protected
	pass
	
class SignupForm(UserCreationForm):
  
    
    class Meta:
        model = User
        fields = ('username','password1','password2')#default


   