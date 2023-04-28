from django.urls import path
from .views import *
urlpatterns = [
	path("create_community/",CommunityCreation.as_view(),name='create_community'),
	path("create_room/<id>/",RoomCreation.as_view(),name="create_room"),
	path("community_details/<id>/",CommunityInfo.as_view(),name="community_details"),
	path("create_post/<id>/",CreatePost.as_view(),name="create_post"),
	path("join_community/<id>",SubscribeToCommunity.as_view(),name="join_community"),
	path('roominfo/<id>/',RoomDet.as_view(),name="roominfo"),
	path('room_list/<id>/',RoomList.as_view(),name='room_list'),
	path('room_update/<id>/',ModifyRoom.as_view(),name = "room_update"),
	path('room_delete/<id>/',DeleteRoom.as_view(),name = "room_delete"),
	path('delete_message/<id>/',DeleteMessage.as_view(),name="delete_message"),
]