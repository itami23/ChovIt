
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Community(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	members = models.ManyToManyField(User,related_name="community_members")
	author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="community_author")
	image = models.ImageField(blank=True , null = True , upload_to = 'Community_Images')

	# class Meta:
	# 	ordering=["name"]

	def __str__(self):
		return self.name




class Room(models.Model):
	host=models.ForeignKey(User, on_delete=models.CASCADE)
	#topic=models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
	name=models.CharField(max_length=100)
	description=models.TextField(null=True,blank=True)
	participants=models.ManyToManyField(User,related_name='participants',blank=True)
	updated=models.DateTimeField(auto_now=True)
	created=models.DateTimeField(auto_now_add=True)
	community = models.ForeignKey(Community, on_delete=models.SET_NULL,null=True)
	image = models.ImageField(blank=True , null = True , upload_to = 'Room_Images')

	class Meta:
		ordering=['-updated','-created']

	def __str__(self):
		return self.name


class Message(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	room=models.ForeignKey(Room, on_delete=models.CASCADE)
	body=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	class Meta:
		ordering=['-updated','-created']

	def __str__(self):
		return self.body[0:50]


class Post(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	community = models.ForeignKey(Community, on_delete=models.CASCADE)
	body = models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	image = models.ImageField(blank=True , null = True , upload_to = 'Posts_Images')

	class Meta:
		ordering = ["-updated","-created"]

	def __str__(self):
		return self.body[0:50]



