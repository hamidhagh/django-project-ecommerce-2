from django import forms
from .models import Comment


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
