from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(username=data['username'],email=data['email'],first_name=data['first_name'],
                                     last_name=data['last_name'], password=data['password_1'])
            return redirect('home:home')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, 'account/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request,username=User.objects.get(email=data['user']),password=data['password'])
            except:
                user = authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                return redirect('home:home')
            
    else:
        form = UserLoginForm()
    context = {'form':form}
    return render(request, 'account/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home:home')
