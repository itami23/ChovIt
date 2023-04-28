from django.shortcuts import render
from django.views import View
from Chat.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
######################################
from django.urls import reverse
from itertools import chain
from django.db.models import Q
######################################
# Create your views here.
class Home(View):
	def get(self,request,*args,**kwargs):
		if self.request.GET.get("q")!=None:
			q=self.request.GET.get("q")
		else :
			q=''

		c = Community.objects.filter(
			Q(name__icontains=q) |
			Q(description__icontains=q)
		)	

		p=Paginator(c, 10)
		page_num = request.GET.get("page")
		communities = p.get_page(page_num)
		nums = "a" * communities.paginator.num_pages
		comms = Community.objects.all()
		comm_count = comms.count()
		context = {
			'communities' : communities,
			"nums" : nums,
			'comm_count' : comm_count,
		}
		return render(request, 'Main/home.html',context)



class FeedPage(View):
	@method_decorator(login_required(login_url="login_user"))
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)

	def get(self,request,*args,**kwargs):
		communities = []
		posts = []
		qs=None
		for comm in Community.objects.all():
			if request.user in comm.members.all():
				communities.append(comm)

		for comm in communities :
			c_posts = comm.post_set.all()
			posts.append(c_posts)

		if posts :
			if len(posts)>0:
				qs = sorted(chain(*posts), reverse=True, key=lambda obj:obj.created)

		# paginator = Paginator(qs, 5)
		# page = request.GET.get('page')
		# posts_list = paginator.get_page(page)
		

		context = {
			'communities' : communities,
			'posts':qs,
		}
		return render(request, 'Main/feeds.html',context)
