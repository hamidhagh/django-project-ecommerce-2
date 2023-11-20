import django_filters
from django import forms
from .models import *



class ProductFilter(django_filters.FilterSet):

    choice_1 = {
        ('expensive','expensive'), #('گران ترین','گران ترین')
        ('cheap','cheap'),
    }

    choice_2 = {
        ('old','old'),
        ('new','new'),
    }


    choice_3 = {
        ('less_popular','less_popular'),
        ('more_popular','more_popular'),
    }

    price_start = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_end = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=choice_1, method='price_filter')
    created_time = django_filters.ChoiceFilter(choices=choice_2, method='created_time_filter')
    favorite = django_filters.ChoiceFilter(choices=choice_3, method='favorite_filter')
    


    def price_filter(self,queryset,name,value):
        data = 'price' if value == 'cheap' else '-price'
        return queryset.order_by(data)
    


    def created_time_filter(self,queryset,name,value):
        data = 'created_time' if value == 'old' else '-created_time'
        return queryset.order_by(data)
    


    def favorite_filter(self,queryset,name,value):
        data = 'total_favorite' if value == 'less_popular' else '-favorite'
        return queryset.order_by(data)