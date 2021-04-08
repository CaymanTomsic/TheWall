from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    if 'user_id' in request.session:
        return redirect("/wall")
    else:
        return render(request, "index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect("/")
    else:
        hash_browns= bcrypt.hashpw(request.POST['password_form'].encode(), bcrypt.gensalt()).decode()
        created_user = User.objects.create(
            username = request.POST['username_form'],
            email = request.POST['email_form'],
            birthday = request.POST['birthday_form'],
            password = hash_browns,
        )
        request.session['user_id'] = created_user.id
        return redirect("/wall")

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect("/")
    else:
        user = User.objects.get(email=request.POST['log_email'])
        request.session['user_id'] = user.id
        return redirect("/wall")

def logout(request):
    request.session.flush()
    return redirect('/')

def wall(request):
    if 'user_id' not in request.session:
        return redirect("/")
    else:
        user_id = request.session['user_id']
        context={
        'selected_user': User.objects.get(id=user_id),
        'all_message': PostedMessage.objects.all()
        }
        return render(request, "wall.html", context)

def create_message(request):
    errors = User.objects.validate_message(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect("/wall")
    else:
        user_id = request.session['user_id']
        created_message = PostedMessage.objects.create(
            user = User.objects.get(id=user_id),
            message_text = request.POST['message_text_form']
        )
        print(created_message)
        return redirect("/wall")

def destroy_message(request, message_id):
    message_to_destroy = PostedMessage.objects.get(id=message_id)
    message_to_destroy.delete()
    return redirect("/wall")

def create_comment(request, message_id):
    errors = User.objects.validate_comment(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect("/wall")
    else:
        user_id = request.session['user_id']
        created_comment = Comment.objects.create(
            user = User.objects.get(id=user_id),
            posted_message = PostedMessage.objects.get(id=message_id),
            comment_text = request.POST['comment_text_form']
        )
        print(created_comment)
        return redirect("/wall")