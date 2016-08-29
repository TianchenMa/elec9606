from django import forms


class CommentForm(forms.Form):
    author_id = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

