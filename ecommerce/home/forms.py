from django import forms
from .models import Comment, Compare


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rate']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)



class CompareForm(forms.ModelForm):
    class Meta:
        model = Compare
        fields = ['product']
