from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponseRedirect
from .forms import UploadPicForm
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    return render (request,'login.html')

def success(request):
    if "user_id" not in request.session:
        return redirect('/')

    context={
        "posts": Post.objects.all(),
        "comments":Comment.objects.all()
    }

    return render (request,'main_page.html', context) 

def register_page(request):
    return render(request,'register.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request,error)
            return redirect('/')

 
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
     
    
    user = User.objects.create(first_name=request.POST['first_name'],last_name = request.POST['last_name'],email = request.POST['email'], password=pw_hash) 
    
    request.session["user_id"] = user.id
    request.session["user_name"] = user.first_name
    return redirect('/wall')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email)

        if user: 
            logged_user = user[0] 
       
            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
           
                request.session['user_id'] = logged_user.id
                request.session["user_name"] = logged_user.first_name
            
                return redirect('/wall')
            else:
                messages.error(request,"This password is incorrect!")
                return redirect('/')
        else:
            messages.error(request,"This User doesn't exist!")
            return redirect('/')
    
    return redirect('/')

def logout(request):
    request.session.flush()

    return redirect('/')

def profile(request,id):
    user=User.objects.get(id=id)
    posts=Post.objects.filter(poster=user)

    context = {
        "user":user,
        "posts":posts,
        "comments":Comment.objects.all()
    }
    return render(request,'profile.html',context)

def profile_edit(request,id):
    user=User.objects.get(id=id)
    if request.method == "GET":
        context = {
        "user":user
    }
        return render(request,'edit_profile.html', context)
    else:
        #Causing error
        errors = User.objects.profile_validator(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request,error)
            return redirect(f'/profile/edit/{user.id}')    
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.phone = request.POST["phone"]
        user.city = request.POST["city"]
        user.save()
        return redirect(f'/profile/{user.id}')

def profile_pic(request,id):
    user=User.objects.get(id=id)
    
    if len(request.FILES) != 0:
        user.profile_pic = request.FILES["profile_pic"]
        user.save()

        return redirect(f'/profile/{user.id}')
    else:
        return redirect(f'/profile/edit/{user.id}')

def create_post(request):
    if len(request.FILES) != 0:
        poster = User.objects.get(id=request.session["user_id"])

        Post.objects.create(picture=request.FILES["pic"], desc=request.POST["desc"], poster=poster)

        return redirect('/wall')
    else:
        return redirect('/wall')

def create_comment(request,id):

    poster = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=id)
    
    Comment.objects.create(comment=request.POST["comment"],poster=poster,post=post)

    return redirect('/wall')

def like_post(request,id):
    user = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=id)
    post.likes.add(user)
    return redirect('/wall')

def like_com(request,id):
    user = User.objects.get(id=request.session["user_id"])
    comment = Comment.objects.get(id=id)
    comment.likes.add(user)
    return redirect('/wall')

def delete_post(request,id):
    user = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=id)
    post.delete()

    return redirect(f'/profile/{user.id}')

def delete_com(request,id):
    user = User.objects.get(id=request.session["user_id"])
    comment = Comment.objects.get(id=id)
    comment.delete()

    return redirect('/wall')

def edit_post(request,id):
    user = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=id)
    if request.method == "GET":
        context = {
        "user":user,
        "post":post,
    }
        return render(request,'edit_post.html', context)
    if len(request.FILES) != 0:
        post.picture = request.FILES["pic"]
        post.desc = request.POST["desc"]
        post.save()
        return redirect(f'/profile/{user.id}')
    else:
        post.desc = request.POST["desc"]
        return redirect(f'/profile/{user.id}')
    