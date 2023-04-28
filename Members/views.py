from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Chat.models import *

# Create your views here.
class Register(View):
	def get(self,request,*args,**kwargs):
		form=UserRegisterForm()
		context={
			'form' : form,
		}
		return render(request, 'Members/register.html',context)


	def post(self,request,*args,**kwargs):
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login_user')

		context={
			'form' : form,
			
		}
		return render(request, 'Members/register.html',context)


class LoginUser(View):
	def get(self,request,*args,**kwargs):
		context={
			
		}
		return render(request, 'Members/login_user.html',context)


	def post(self,request,*args,**kwargs):
		username=request.POST['username']
		password=request.POST["password"]
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request, user)
			return redirect('home')

		else:
			messages.error(request, "Invalid Credentials")
			return redirect('login_user')

		context={
			
		}
		return render(request, 'Members/login_user.html',context)


def logout_user(request):
	logout(request)
	return redirect('home')


class ProfileView(View):
	@method_decorator(login_required(login_url='login_user'))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		u=User.objects.get(pk=self.kwargs.get('id'))
		communities = []
		for comm in Community.objects.all():
			if request.user in comm.members.all():
				communities.append(comm)
		user_posts = u.post_set.all()
		context = {
			'user' : u,
			'posts' : user_posts,
			'communities' : communities,
		}
		return render(request, "Members/profile.html",context)


class EditProfile(View):
	
	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		form = UserProfileForm(instance=request.user.profile)
		context = {
			'form' : form,
		}
		return render(request, "Members/profile_edit.html",context)

	def post(self,request,*args,**kwargs):
		form = UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
		if form.is_valid():
			form.save()
			return redirect('profile',id =request.user.id)
		context = {
			'form' : form,
		}
		return render(request, "Members/profile_edit.html",context)