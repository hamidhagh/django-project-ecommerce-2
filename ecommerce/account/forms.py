from django import forms
from django.contrib.auth.models import User
from .models import Profile

#from django.contrib.auth.forms import ReadOnlyPasswordHashField


error = {
    'required': 'این فیلد اجباری است!',
    'invalid': 'ایمیل نامعتبر است'
}



class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=255,error_messages=error,widget=forms.TextInput(attrs={'placeholder':'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email'}))
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    password_1 = forms.CharField(max_length=255,widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    password_2 = forms.CharField(max_length=255,widget=forms.PasswordInput(attrs={'placeholder':'password'}))


    def clean_user_name(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('username exists!')
        return user
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email exists!')
        return email
    
    def clean_password_2(self):
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']
        if password_1 != password_2:
            raise forms.ValidationError('password not match!')
        elif len(password_2) < 8:
            raise forms.ValidationError('password too short!')
        elif not any(x.isupper() for x in password_2):
            raise forms.ValidationError('password must contain at least one capital letter!')
        return password_2
    


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    remember = forms.BooleanField(required=False,widget=forms.CheckboxInput())



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','address', 'photo']


# class PhoneForm(forms.Form):
#     phone = forms.IntegerField()


# class PhoneVerifyForm(forms.Form):
#     code = forms.IntegerField()




#custom user model

# class UserCreateForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ['email','username','phone']

#         def clean_password2(self):
#             data = self.cleaned_data
#             if data['password2'] and data['password1'] and data['password2'] != data['password1']:
#                 raise forms.ValidationError('wrong')
#             return data['password2']
        

#         def save(self,commit=True):
#             user = super().save(commit=False)
#             user.set_password(self.cleaned_data['password2'])
#             if commit:
#                 user.save()
#             return user
        

# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField
#     class Meta:
#         model = User
#         fields = ['email','username','phone']


#     def clean_password(self):
#         return self.initial['password']