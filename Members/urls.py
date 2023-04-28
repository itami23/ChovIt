from django.urls import path
from .views import *
urlpatterns = [
	path('register/',Register.as_view(),name='register'),
	path('login_user/',LoginUser.as_view(),name='login_user'),
	path('logout_user/',logout_user,name="logout_user"),
	path('profile/<id>',ProfileView.as_view(),name='profile'),
	path('edit_profile/',EditProfile.as_view(),name='edit_profile'),
]