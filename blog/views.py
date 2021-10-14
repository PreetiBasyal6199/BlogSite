from django.contrib import auth
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .forms import blogForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import response
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import User, blog
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .forms import UserRegisterForm
from django.urls import reverse_lazy
# Create your views here.


def Home(request):
    posts = blog.objects.all()
    return render(request, 'BLOGAPP/home.html', {'posts': posts})


@csrf_protect
def UserRegisterView(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(
                request, 'The email address is already registered...')
            return render(request, 'BLOGAPP/register.html', {'form': form})
        elif pw1 != pw2:
            messages.error(request, 'Two passwords donnot match...')
            return render(request, 'BLOGAPP/register.html', {'form': form})

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
        messages.error(
            request, 'Invalid Password..Password must containat least 10 characters and minimum a numeric and a special character')
        return render(request, 'BLOGAPP/register.html', {'form': form})

    return render(request, 'BLOGAPP/register.html', {'form': form})


@csrf_exempt
def LoginView(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                blogs = blog.objects.filter(author_id=request.user.id)
                return render(request, "BLOGAPP/AfterLogin.html", {'obj': blogs})

        messages.error(request, 'Invalid Username or Password...')
        return render(request, 'BLOGAPP/login.html', {'form': form})

    return render(request, 'BLOGAPP/login.html', {'form': form})


def UserLogoutView(request):
    logout(request)
    return HttpResponseRedirect('/')


def blogPost(request):
    form = blogForm(request.POST)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return HttpResponseRedirect('/view_blog/')
    return render(request, "BLOGAPP/PostBlog.html", {"form": form})


@login_required
def viewBlog(request):
    blogs = blog.objects.filter(author_id=request.user.id)
    return render(request, 'BLOGAPP/AfterLogin.html', {'obj': blogs})


def BlogDetailView(request, pk):
    post = blog.objects.get(id=pk)
    return render(request, 'BLOGAPP/View_Single_Blog.html', {'obj': post})


def BlogEditView(request, pk):
    if request.method == "POST":
        blogs = blog.objects.get(id=pk)
        form = blogForm(request.POST, instance=blogs)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/view_blog/')
    else:
        blogs = blog.objects.get(id=pk)
        form = blogForm(instance=blogs)

    return render(request, 'BLOGAPP/Edit_Blog.html', {'form': form})


def DeleteBlogView(request, pk):
    item = blog.objects.get(id=pk)
    item.delete()
    blogs = blog.objects.filter(author_id=request.user.id)
    return render(request, 'BLOGAPP/AfterLogin.html', {'obj': blogs})


def SearchResult(request):
    item = request.GET.get('catagory')
    items = blog.objects.filter(catagory=item)
    if items:
        return render(request, 'BLOGAPP/SearchResult.html', {'items': items})
    else:
        messages.error(request, 'No blogs in the catagory')
        return render(request, 'BLOGAPP/SearchResult.html', {'item': item})
