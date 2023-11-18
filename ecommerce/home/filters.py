import django_filters
from django import forms
from .models import *



class ProductFilter(django_filters.FilterSet):
    price_start = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_end = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)