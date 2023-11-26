from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
# from django.core.mail import EmailMessage
# from django.views import View
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from six import text_type
# from django.urls import reverse

from random import randint

from .models import Profile
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm

from order.models import OrderItem
from home.models import Product, View




# class EmailToken(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))
    
# email_generator = EmailToken()


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'],email=data['email'],first_name=data['first_name'],
                                     last_name=data['last_name'], password=data['password_1'])
            #user.is_active = False
            user.save()
            # domain = get_current_site(request).domain
            # uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            # url = reverse('email-register', kwargs={'uidb64':uidb64,'token':email_generator.make_token()})
            # link = 'http://'+ domain + url
            # email = EmailMessage(
            #     'active user',
            #     link,
            #     'hamidhaghverdi12345@gmail.com',
            #     [data['email']],
            # )
            # email.send(fail_silently=False)
            messages.success(request,'check your email','success')
            return redirect('home')
    else:
        form = UserRegisterForm()
    # if request.user.is_authenticated:
    #     return redirect('home')
    context = {'form':form}
    return render(request, 'account/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            remember = data['remember']
            try:
                user = authenticate(request,username=User.objects.get(email=data['username']),password=data['password'])
            except:
                user = authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                if not remember:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(100000)
                messages.success(request,'Welcome!','primary')
                return redirect('home')
            else:
                messages.error(request,'login failed!','danger')
            
    else:
        form = UserLoginForm()
    # if request.user.is_authenticated:
    #     return redirect('home')
    context = {'form':form}
    return render(request, 'account/login.html', context)




# class EmailRegister(View):
#     def get(self,request):
#         id = force_text(urlsafe_base64_decode())
#         return redirect('user_login')

    



@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    messages.success(request,'logout successful!','primary')
    return redirect('home')


@login_required(login_url='user_login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'account/profile.html', {'profile':profile})



@login_required(login_url='user_login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
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



# def login_phone(request):
#     if request.method == 'POST':
#         form = PhoneForm(request.POST)
#         if form.is_valid():
#             global random_code, phone
#             data = form.cleaned_data
#             phone = f"0{data['phone']}"
#             random_code = randint(100,1000)
#             #sms service
#             return redirect('phone_verify')

#     else:
#         form = PhoneForm()
#     return render(request, 'account/login_phone.html', {'form':form})



# def phone_verify(request):
#     if request.method == 'POST':
#         form = PhoneVerifyForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             if random_code == data['code']:
#                 profile = Profile.objects.get(phone=phone)
#                 user = User.objects.get(profile__id = profile.id)
#                 login(request,user)
#                 messages.success(request,'Welcome!','primary')
#                 return redirect('home')
#             else:
#                 messages.error(request,'wrong code!','danger')

#     else:
#         form = PhoneVerifyForm()
#     return render(request, 'account/phone_verify.html', {'form':form})



def favorite_products(request):
    favorite_products = request.user.user_favorite.all()
    return render(request, 'account/favorite-products.html', {'favorite_products':favorite_products})



def history(request):
    data = OrderItem.objects.filter(user_id=request.user.id)
    return render(request, 'account/history.html', {'data':data})



def product_view(request):
    products = Product.objects.filter(view=request.user.id)
    views = View.objects.filter(id=request.META.get('REMOTE_ADDR')).order_by('-created_time')[:2]
    return render(request, 'account/product-view.html', {'products':products})
