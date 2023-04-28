from django.forms import ModelForm
from django import forms
from .models import *

class CommunityForm(ModelForm):
	class Meta:
		model=Community
		fields = '__all__'
		exclude = ["author","members"]


class RoomCreationForm(ModelForm):
	class Meta:
		model=Room
		fields = "__all__"
		exclude = ["host","participants"]



class PostCreationForm(ModelForm):
	class Meta:
		model=Post
		fields = "__all__"
		exclude = ["user","community"]


class MessageForm(ModelForm):
	class Meta:
		model=Message
		fields = "__all__"
		exclude = ['user_room']