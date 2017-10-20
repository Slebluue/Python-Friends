from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from models import User, Friend
import bcrypt
import re

#------------------------ friendship management --------------------------#

#Home Page
def friends(request):
    user = User.objects.get(id=request.session['id'])
    friends = user.friends.all()
    all_users = User.objects.all()

    # Checks for users that are not already friends with the logged in user
    user_list = []
    for u in all_users:
        if u not in friends and u != user:
            user_list.append(u)

    #Friends list should not include the logged in user if accidentally added somehow
    friends_list = []
    for f in friends:
        if f != user:
            friends_list.append(f)

    context = {
        'User': user, 
        'friends': friends_list,
        'users': user_list,
    }
    return render(request , "users/friends.html", context)

def add(request, id):
    user = User.objects.get(id=request.session['id'])
    friend = User.objects.get(id=id)
    ## Add and remove friends. if you want friendhsip to be possible one way remvoe second line
    Friend.objects.create(from_person=user, to_person=friend)
    Friend.objects.create(from_person=friend, to_person=user)
    user.save()

    return redirect('/friends')

def remove(request, id):
    user = User.objects.get(id=request.session['id'])
    friend = User.objects.get(id=id)
    ## Add and remove friends. if you want friendhsip to be possible one way remove second line
    Friend.objects.filter(from_person=user, to_person= friend).delete()
    Friend.objects.filter(from_person=friend, to_person=user).delete()
    return redirect('/friends')

def show(request,id):
    user = User.objects.get(id=id)
    context = {
        'User': user,
    }
    return render(request, "users/show.html", context)

#------------------------ LOGIN CODE --------------------------#
# Load home page
def index(request):
    context = {
        'Users': User.objects.all(),
    }
    return render(request , "users/login.html", context)


def register(request):
    if request.method == "POST":
        #Validation in models.py AND creates user if no errors
        valid, response = User.objects.register_validator(request.POST)
        if valid:
            request.session['id'] = response.id
            return redirect('/friends')
        else:
            for message in response:
                messages.error(request, message)
            return redirect('/')
    else:
        return redirect('/')

def login(request):
    if request.method == "POST":
        #Validation in models.py
        valid, response = User.objects.login_validator(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if valid:
            request.session['id'] = response.id
            return redirect("/friends")
        else:
            for message in response:
                messages.error(request, message)
            return redirect('/')
         
def logout(request):
    if request.method == "POST":
        del request.session['id']
        return redirect("/")
    else:
        del request.session['id']
        return redirect("/")

