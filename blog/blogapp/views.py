from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .form import *

# Create your views here.

def base(request):
    return render(request, 'base.html')


@login_required(login_url='/login_page')
def homepage(request):
    return render(request, 'homepage.html')

#Adding blogs 
def add_blogs(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES['image']
            title = request.POST['title']
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            BlogModel.objects.create(
                user = user, title = title, content = content, image = image,
            )
            return redirect('/homepage')

    except Exception as e:
        print(e)
    return render(request, 'add_blogs.html', context)

    


# AUTHENTICATIONS

def signup_page(request):
    
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        
        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, 'Username already Exist!')
            return redirect('/signup_page')
        
        user = User.objects.create(
                email = email, 
                username = username,
                first_name = first_name,
                last_name = last_name,
            
        )
        user.set_password(password)
        user.save()
        print(f"{user.first_name} Your account has been created Successfully!")
        messages.success(request, f"Hello {first_name}, Your account has been created Successfully!")
        return redirect('/signup_page')

    return render (request, 'signup_page.html')

# LOGIN
def login_page(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username!")
            return redirect('/login_page')

        user = authenticate(username = username, password = password)
    
        if user is None:
            messages.error(request, "Incorrect Password!")
            return redirect('/login_page')
        else:
            login(request, user)
            return redirect('/homepage')
            
    return render (request, 'login_page.html')


# LOGOUT
def logout_page(request):

    logout(request)
    return redirect('/login_page')

