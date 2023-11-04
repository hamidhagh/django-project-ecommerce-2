from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm



def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'],email=data['email'],first_name=data['first_name'],
                                     last_name=data['last_name'], password=data['password_1'])
            user.save()
            messages.success(request,'register successful!','success')
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
                messages.success(request,'Welcome!','primary')
                return redirect('home:home')
            else:
                messages.error(request,'login failed!','danger')
            
    else:
        form = UserLoginForm()
    context = {'form':form}
    return render(request, 'account/login.html', context)


@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    messages.success(request,'logout successful!','primary')
    return redirect('home:home')


@login_required(login_url='user_login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'account/profile.html')



@login_required(login_url='user_login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'update successful','success')
            return redirect('user_profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'user_form':user_form,'profile_form':profile_form}
    return render(request,'account/update.html',context)



@login_required(login_url='user_login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, 'password changed!','success')
            return redirect('user_profile')
        else:
            messages.error(request, 'password change failed!','danger')
            return redirect('change_password')
        
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html',{'form':form})