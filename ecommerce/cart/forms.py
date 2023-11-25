from django import forms
from .models import Cart



class CartForm(forms.Form):
    quantity = forms.IntegerField()