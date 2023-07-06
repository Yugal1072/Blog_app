from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .form import *
from django.core.mail import send_mail

# Create your views here.

def base(request):
    return render(request, 'base.html')


@login_required(login_url='/login_page')
def homepage(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'homepage.html', context)

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
            
            #Mail sending 
            
            subject = "Blog app"
            message = f'Your blog {title} has been Created!'
            email_from = 'yugalgovind@gmail.com'
            recipient_list = ['yugalgovind1072@gmail.com']
            send_mail(subject, message, email_from, recipient_list)
            
            return redirect('/homepage')

    except Exception as e:
        print(e)
    return render(request, 'add_blogs.html', context)


#API comment
def postComment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        user = request.user
        post = request.POST['post']
        parent = request.POST['parent']
        
        comments = BlogComment.objects.create(comment = comment,
                    user = user,
                    post = post,
                    parent = parent,)
        context = {'comments':comments}
        return redirect(f'/{postComment.slug}')

    return render(request, 'blog_detail.html', context)
    
def blog_detail(request, slug):
    context = {}
    try:
        blog_object = BlogModel.objects.filter(slug = slug).first()
        comments = BlogComment.objects.filter(post = blog_object)
        context ={ "blog_object": blog_object, "comments":comments}
    except Exception as e:
        print(e)
    return render (request, 'blog_detail.html', context)


# AUTHENTICATIONS API's
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

