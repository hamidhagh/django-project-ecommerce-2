from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_delete,pre_save,post_delete,m2m_changed
#from django.core.signals import request_finished,request_started
from phone_field import PhoneField



class Profile(models.Model):
    phone = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    


def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile9user=kwargs['instance']
        profile_user.save()
post_save.connect(save_profile_user,sender=User)