from django import  forms
from .models import Order



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'first_name', 'last_name', 'address']



class DiscountCodeForm(forms.Form):
    code = forms.CharField(max_length=100)