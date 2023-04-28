from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
# Create your views here.
class CommunityCreation(View):

	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)
		

	def get(self,request,*args,**kwargs):
		form = CommunityForm()
		context={
			'form' : form,
		}
		return render(request, 'Chat/community_form.html',context)

	def post(self,request,*args,**kwargs):
		form = CommunityForm(request.POST,request.FILES)
		if form.is_valid():
			f=form.save(commit=False)
			f.author=request.user
				
			f.save()
			f.members.add(request.user)
			f.save()
			return redirect('home')

		context = {
			'form' : form,
		}
		return render(request, 'Chat/community_form.html',context)


class RoomCreation(View):
	@method_decorator(login_required(login_url = "login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)


	def get(self,request,*args,**kwargs):
		form = RoomCreationForm()
		
		communities = Community.objects.all()
		context = {
			'form' : form,
			
			
		}
		return render(request, 'Chat/room_form.html',context)


	def post(self,request,*args,**kwargs):
		form = RoomCreationForm(request.POST,request.FILES)
		
		community = Community.objects.get(pk=self.kwargs.get("id"))
		

		a=Room.objects.create(
			host=request.user,
			name = request.POST.get('name'),
			description=request.POST.get("description"),
			community = community,
			image = request.POST.get("image"),
			)
		a.save()
		a.participants.add(request.user)

		return redirect("community_details",id=self.kwargs.get("id"))



class CommunityInfo(View):

	@method_decorator(login_required(login_url = "login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)


	def get(self,request,*args,**kwargs):
		a = ""
		comm = get_object_or_404(Community,id = self.kwargs.get("id"))
		if request.user in comm.members.all():
			a = "Leave Community"
		else : 
			a = "Join Community"
		rooms = comm.room_set.all()[0:4]
		posts = comm.post_set.all()
		context = {
			'comm' : comm,
			'rooms' : rooms,
			'posts' : posts,
			'a' : a,
		}
		return render(request, 'Chat/community_detail.html',context)


class SubscribeToCommunity(View):

	@method_decorator(login_required(login_url = 'login_user'))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)


	def get(self,request,*args,**kwargs):
			ok = ""
			comm=Community.objects.get(pk=self.kwargs.get("id"))
			members = comm.members.all()
			if request.user in members :
				comm.members.remove(request.user)
			else : 
				comm.members.add(request.user)
				comm.save()

			return redirect("community_details",id=self.kwargs.get("id"))

			

	def post(self,request,*args,**kwargs):
		pass



class CreatePost(View):
	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		form = PostCreationForm()
		context = {
			"form" : form,
		}

		return render(request, "Chat/post_form.html",context)



	def post(self,request,*args,**kwargs):
		form = PostCreationForm(request.POST,request.FILES)
		if form.is_valid():
			f = form.save(commit=False)
			f.user=request.user
			f.community = Community.objects.get(pk=self.kwargs.get("id"))
			f.save()
			return redirect("community_details",id=self.kwargs.get("id"))

		context = {
			"form" : form,
		}
		return render(request, "Chat/post_form.html",context)



class RoomDet(View):
	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		#form = MessageForm()
		room = Room.objects.get(id = self.kwargs.get('id'))
		messages = room.message_set.all()
		participants = room.participants.all()
		context = {
			'room' : room,
			'messages' : messages,
			'participants': participants,
		}
		return render(request, "Chat/room_info.html",context)


	def post(self,request,*args,**kwargs):
		#form=MessageForm(request.POST)
		room=Room.objects.get(pk=self.kwargs.get('id'))
		message = Message.objects.create(
			user = request.user,
			room = room,
			body = request.POST.get('body')
		)
		room.participants.add(request.user)
		return redirect('roominfo',id=self.kwargs.get("id"))


class RoomList(View):
	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		community = Community.objects.get(id = self.kwargs.get("id"))
		rooms = community.room_set.all()
		context = {
			"rooms" : rooms
		}
		return render(request, "Chat/room_list.html",context)



class ModifyRoom(View):
	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		room = Room.objects.get(id = self.kwargs.get("id"))
		form = RoomCreationForm(instance=Room.objects.get(id = self.kwargs.get("id")))
		if request.user != room.host :
			return redirect('roominfo',id=self.kwargs.get("id"))
		context = {
			'form' : form,
		}
		return render(request, "Chat/room_form.html",context)

	def post(self,request,*args,**kwargs):
		form = RoomCreationForm(request.POST,instance=Room.objects.get(id = self.kwargs.get("id")))
		room = Room.objects.get(id = self.kwargs.get("id"))
		room.name = request.POST.get("name")
		room.description = request.POST.get("description")
		room.save()
		return redirect('roominfo',id=self.kwargs.get("id"))



class DeleteRoom(View):

	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		room = Room.objects.get(id = self.kwargs.get("id"))
		if request.user != room.host :
			return redirect('roominfo', id = room.id)
		else :
			a = room.name
			context = { 
			'a' : a,
			}
			return render(request, "Chat/delete.html",context)
		

	def post(self,request,*args,**kwargs):
		room = Room.objects.get(id = self.kwargs.get("id"))
		if request.user != room.host :
			return redirect('roominfo', id = room.id)
		else :
			comm = room.community.id
			room.delete()
			return redirect('community_details' , id = comm)


class DeleteMessage(View):
	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		message = Message.objects.get(pk=self.kwargs.get("id"))
		if message.user == request.user:
			message.delete()
			return redirect(request.META.get('HTTP_REFERER'))
		else :
			return redirect(request.META.get('HTTP_REFERER'))