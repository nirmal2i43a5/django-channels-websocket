from django.shortcuts import render,reverse,redirect,resolve_url

# from django.http import Htt

from django.contrib.auth.views import LoginView,LogoutView,FormView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from .forms import SignupForm,LoginForm


def LoginView(request):
	form = LoginForm()

	if request.method == 'POST':
		username = request.POST.get('username')#grabing username from form input value
		password =request.POST.get('password')
		
		user = authenticate(request, username=username, password=password)
  
		if user is not None:
			login(request, user)
   
			return redirect('chat:user',username)#for url messages/username
		else:
			return redirect('/admin/')
		

	context = {'form':form}
	return render(request, 'login.html', context)
	

		
class SignupView(CreateView):
	template_name = 'signup.html'
	form_class = SignupForm
	success_url = '/login/'
	
	
		