from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("register/", views.register, name="register"),
	path("add_user/", views.add_user, name="add_user"),
	path("profile/", views.profile, name="profile"),
	path("messages/", views.messages, name="messages"),
	path("send_message/", views.send_message, name="send_message"),
	path("remove_message/", views.remove_message, name="remove_message"),
    path("logout/", views.logout, name="logout")
]
