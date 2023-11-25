from django.contrib import admin
from .models import Profile

# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import *
# from .models import User
# from django.contrib.auth.models import Group

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','address']


admin.site.register(Profile,ProfileAdmin)


#custom user model

# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreateForm
#     list_display = ['email', 'username', 'phone']
#     list_filter = ['email', 'is_active']
#     fieldsets = (
#         ('User',{'fields':('email','password')}),
#         ('Personal info',{'fields':('is_admin',)}),
#         ('Permissions',{'fields':('is_active',)}),
#     )

#     add_fieldsets = (
#         (None,{'fields':('email','username','phone','password1','password2')}),
#     )

#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()

# admin.site.register(User,UserAdmin)
# admin.site.unregister(Group)