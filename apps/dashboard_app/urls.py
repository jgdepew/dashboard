from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login$', views.login, name='login'),
	url(r'^process_login$', views.process_login, name='process_login'),
	url(r'^register$', views.register, name='register'),
	url(r'^process_registration$', views.process_registration, name='process_registration'),
	url(r'^process_logout$', views.process_logout, name='process_logout'),
	url(r'^dashboard$', views.admin, name='dashboard'),
	url(r'^users$', views.users, name='users'),
	url(r'^users/new$', views.new, name='new'),
	url(r'^users/(?P<id>\d+)/$', views.users_id, name='users_id'),
	url(r'^users/(?P<id>\d+)/delete$', views.delete, name='delete'),
	url(r'^users/(?P<id>\d+)/update$', views.update, name='update'),
	url(r'^users/(?P<id>\d+)/process_message$', views.process_message, name='process_message'),
	url(r'^users/(?P<id>\d+)/process_comment$', views.process_comment, name='process_comment'),

]