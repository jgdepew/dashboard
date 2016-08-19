from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages
import bcrypt

# Create your models here.
class ValidationManager(models.Manager):
	def registrationValidator(self, request, email, first_name, last_name, password1, password2):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = 0
		if  len(User.objects.all()) < 1:
			user_level = 9
		else: 
			user_level = 1

		if len(email)<1:
			messages.error(request, 'No email entered')
			errors += 1
		elif not EMAIL_REGEX.match(email):
			messages.error(request, 'Not a valid email.')
			errors += 1	
		elif User.objects.filter(email=email):
			messages.error(request, 'Email already in use.')
			errors += 1

		if len(first_name) < 2 or len(last_name) < 2:
			messages.error(request, 'Names are not valid.')
			errors += 1

		if password1 != password2:
			messages.error(request, 'Passwords do not match.')
			errors += 1			
		elif len(password1)<4:
			messages.error(request, 'Not a valid password.')
			errors += 1			

		if errors > 0:
			return False
		else:
			password = str(request.POST['password1'])
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed, user_level=user_level, description=None)
			return True
	def loginValidator(self, request, password, email):
		if len(User.objects.filter(email=email))<1:
			messages.error(request, 'Invalid login information.')
			return False
		user = User.objects.get(email=email)
		password_entered = password.encode()
		hashed_entered = bcrypt.hashpw(password_entered, bcrypt.gensalt())
		if email == user.email and bcrypt.hashpw(password_entered, user.password.encode()) == user.password:
			request.session['name'] = user.first_name
			request.session['user_level'] = user.user_level
			request.session['id'] = user.id
			request.session['email'] = user.email
			return True
		else: 
			messages.error(request, 'Password incorrect.')
			return False

class UserManager(models.Manager):
	def edit_information(self, request, id, form_info):
		errors = 0
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if 'user_level' in form_info:
			email = form_info['email']
			first_name = form_info['first_name']
			last_name = form_info['last_name']
			user_level = form_info['user_level']
			if len(email)<1:
				messages.error(request, 'No email entered')
				errors += 1
			elif not EMAIL_REGEX.match(email):
				messages.error(request, 'Not a valid email.')
				errors += 1	

			if len(User.objects.filter(email=email)) > 1: 
				filtered_email = User.objects.get(email=email)
				edit_email = User.objects.get(id=id)
				if filtered_email and filtered_email != edit_email:
					messages.error(request, 'Email already in use.')
					errors += 1

			if len(first_name) < 2 or len(last_name) < 2:
				messages.error(request, 'Names are not valid.')
				errors += 1	
			if errors > 0:
				return False
			else:
				user = User.objects.get(id=id)
				user.first_name = first_name
				user.last_name = last_name
				user.email = email
				user.user_level = user_level
				user.save()
				return True
		elif 'user_level' not in form_info:
			email = form_info['email']
			first_name = form_info['first_name']
			last_name = form_info['last_name']
			if len(email)<1:
				messages.error(request, 'No email entered')
				errors += 1
			elif not EMAIL_REGEX.match(email):
				messages.error(request, 'Not a valid email.')
				errors += 1	

			if len(User.objects.filter(email=email)) > 1: 
				filtered_email = User.objects.filter(email=email)
				if filtered_email and request.session['email'] != email:
					messages.error(request, 'Email already in use.')
					errors += 1

			if len(first_name) < 2 or len(last_name) < 2:
				messages.error(request, 'Names are not valid.')
				errors += 1	
			if errors > 0:
				return False
			else:
				user = User.objects.get(id=id)
				user.first_name = first_name
				user.last_name = last_name
				user.email = email
				user.save()
				return True
		else:
			return False
	def edit_description(self, request, id, form_info):	
		if 'description' in form_info:
			user = User.objects.get(id=id)
			user.description = form_info['description']
			user.save()
			return True
		else: 
			return False
	def edit_password(self, request, id, form_info):
		if 'password1' in form_info:
			password1 = form_info['password1']
			password2 = form_info['password2']
		else:
			return False
		errors = 0
		if password1 != password2:
			messages.error(request, 'Passwords do not match.')
			errors += 1			
		elif len(password1)<4 and len(password2)<4:
			messages.error(request, 'Not a valid password.')
			errors += 1	
		if errors > 0:
			return False
		else:
			user = User.objects.get(id=id)
			password = str(password1)
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			user.password = hashed
			user.save()
			return True

class PostManager(models.Manager):
	def post_message(self, request, id, form_info):
		user = User.objects.get(id=request.session['id'])
		show = User.objects.get(id=id)
		message = form_info['message']
		Message.objects.create(user=user, show=show, message=message)

	def post_comment(self, request, id, form_info):
		user = User.objects.get(id=request.session['id'])
		message = Message.objects.get(id=form_info['message'])
		comment = form_info['comment']
		Comment.objects.create(user=user, message=message, comment=comment)


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	user_level = models.IntegerField()
	description = models.CharField(max_length=255, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ValidationManager()
	updates = UserManager()

class Message(models.Model):
	user = models.ForeignKey(User)
	show = models.ForeignKey(User, related_name='show')
	message = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = PostManager()

class Comment(models.Model):
	user = models.ForeignKey(User)
	message = models.ForeignKey(Message) 
	comment = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = PostManager()