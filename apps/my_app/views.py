# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import re
import bcrypt
from models import *
EMALI_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    return render(request, 'my_app/index.html')
def register(request):
    error = False
    if len(request.POST['name']) < 3:
        messages.error(request, "name must be at least 4 characters")
        error = True
    if len(request.POST['alias']) < 3:
        messages.error(request, "alias must be at least 4 characters")
        error = True
    if not EMALI_REGEX.match(request.POST['email']):
        messages.error(request, "email is invalid")
        error = True
    if len(request.POST['password']) < 8:
        messages.error(request, "password is too short")
        error = True
    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request, "passwords don't match")
        error = True
    if error:
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        the_user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hash1)
        request.session['user_id'] = the_user.id
        return redirect('/books')
def login(request):
    try:
        the_user = User.objects.get(email=request.POST['email'])

    except: 
        messages.error(request, "email or password are invalid")
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):
        request.session['user_id'] = the_user.id
    else:
        messages.error(request, "email or password are invalid")
    return redirect('/books')
def books(request):
    if not 'user_id' in request.session:
        messages.error(request, "must be logged in")
        request.session['user_id']=0
        return redirect('/')
    context = {
        'User' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'my_app/books.html', context)
def book_add(request):
    if not 'user_id' in request.session:
        messages.error(request, "must be logged in")
        request.session['user_id']=0
        return redirect('/')
    return render(request, 'my_app/add.html')
def book_add_process(request):
    if not request.POST['new_author']:
        author = request.POST['existing_author']
    else:
        author = request.POST['new_author']
    creation = Book.objects.create(title=request.POST['title'], authors=Author.objects.create(name=author))
    # Author.objects.create(name=request.POST['author'])
    Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], reviewer=User.objects.get(id=request.session['user_id']), books=creation)
    return redirect('/books/{}'.format(creation.id))
def review(request, book_id):
    context = {
        "Book" : Book.objects.get(id=book_id),
        "Review" : Review.objects.get(books=book_id)
    }
    return render(request, 'my_app/review.html', context)
def logout(request):
    for key in request.session.keys():
        request.session.clear()
    return redirect('/')