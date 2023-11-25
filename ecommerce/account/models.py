from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_delete,pre_save,post_delete,m2m_changed
from django.dispatch import receiver
#from django.core.signals import request_finished,request_started
from phone_field import PhoneField

#from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class Profile(models.Model):
    phone = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile/', default='default.jpg')

    def __str__(self):
        return self.user.username
    


def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()
        
post_save.connect(save_profile_user,sender=User)

# @receiver(post_save, sender=User)
# def create_profile(sender, instance,created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance,created, **kwargs):
#     instance.profile.save()


#custom user model

# class UserManager(BaseUserManager):
#     def create_user(self,email,username,phone,password):
#         if not email:
#             raise ValueError('please type your email!')
#         if not username:
#             raise ValueError('please type your username!')
#         if not phone:
#             raise ValueError('please type your phone!')
#         user = self.model(email=self.normalize_email(email),username=username,phone=phone)
#         user.set_password(password)
#         user.save(using=self.db)
#         return user
    

#     def create_superuser(self,email,username,phone,password):
#         user = self.create_user(email,username,phone,password)
#         user.is_admin = True
#         user.ssave(using=self.db)
#         return user
        





# class User(AbstractBaseUser):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone= models.IntegerField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     objects = UserManager

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'phone']


#     def __str__(self):
#         return self.email
    

#     def has_perm(self,perm,obj=None):
#         return True
    

#     def has_module_perms(self,app_label):
#         return True
    

#     @property
#     def is_staff(self):
#         return self.is_admin
    

