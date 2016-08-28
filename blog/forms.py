from django import forms
from django.utils.timezone import datetime


class CommentForm(forms.Form):
    author_id = forms.CharField()
    blog_id = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    comment_date = forms.TimeField(datetime.now())
