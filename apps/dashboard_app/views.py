from django.shortcuts import render, redirect, reverse
from .models import User, Message, Comment
# Create your views here.
def users(request):
	if request.method == 'POST':
		return create(request)
	else: 
		return index(request)

def users_id(request, id):
	if request.method == 'POST':
		return process_update(request, id)
	else:
		return show(request, id)

def admin(request):
	if request.session['user_level'] == 9:
		return admin_index(request)
	else:
		return index(request)

def new(request):
	return render(request, 'dashboard_app/new.html')

def create(request):
	if User.objects.registrationValidator(request, request.POST['email'], request.POST['first_name'], request.POST['last_name'], request.POST['password1'], request.POST['password2']):
		return redirect(reverse('dashboard:dashboard'))
	else:
		return redirect(reverse('dashboard:new'))

def show(request, id):
	context = {
		'user': User.objects.get(id=id),
		'messages': Message.objects.filter(show=id),
		'comments': Comment.objects.all(),
	}
	return render(request, 'dashboard_app/show.html', context)

def update(request, id):
	context = {
		'user': User.objects.get(id=id)
	}
	user = User.objects.get(id=id)
	if request.session['id'] == user.id or request.session['user_level'] == 9:
		return render(request, 'dashboard_app/update.html', context)
	else:
		return redirect(reverse('dashboard:dashboard'))

def process_update(request, id):
	if User.updates.edit_information(request, id, request.POST):
		User.updates.edit_information(request, id, request.POST)
		return redirect(reverse('dashboard:users_id', kwargs={'id':id}))
	if User.updates.edit_description(request, id, request.POST):
		User.updates.edit_description(request, id, request.POST)
		return redirect(reverse('dashboard:users_id', kwargs={'id':id}))
	if User.updates.edit_password(request, id, request.POST):
		User.updates.edit_password(request, id, request.POST)
		return redirect(reverse('dashboard:users_id', kwargs={'id':id}))
	return redirect(reverse('dashboard:update', kwargs={'id':id}))

def delete(request, id):
	User.objects.get(id=id).delete()	
	return redirect(reverse('dashboard:dashboard'))

def index(request):
	context = {
		'users': User.objects.all(),
	}
	return render(request, 'dashboard_app/index.html', context)

def admin_index(request):
	context = {
		'users': User.objects.all()
	}
	return render(request,'dashboard_app/admin.html', context)

def login(request):
	return render(request, 'dashboard_app/login.html')

def process_login(request):
	if User.objects.loginValidator(request, request.POST['password'], request.POST['email']):
		User.objects.loginValidator(request, request.POST['password'], request.POST['email'])
		user = User.objects.get(email=request.POST['email'])
		return redirect(reverse('dashboard:dashboard'))
	else:
		return redirect(reverse('dashboard:login'))

def register(request):
	return render(request, 'dashboard_app/register.html')

def process_registration(request):
	if User.objects.registrationValidator(request, request.POST['email'], request.POST['first_name'], request.POST['last_name'], request.POST['password1'], request.POST['password2']):
		return redirect(reverse('dashboard:login'))
	else:
		return redirect(reverse('dashboard:register'))

def process_logout(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect(reverse('dashboard:login'))

def process_message(request, id):
	Message.objects.post_message(request, id, request.POST)
	return redirect(reverse('dashboard:users_id', kwargs={'id': id}))

def process_comment(request, id):
	Comment.objects.post_comment(request, id, request.POST)
	return redirect(reverse('dashboard:users_id', kwargs={'id': id}))
