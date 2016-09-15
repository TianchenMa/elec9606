from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.PasswordInput()


class BlogForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    private = forms.CharField()


class ForwardForm(forms.Form):
    fwdcontent = forms.CharField(max_length=100)
    fwdprivate = forms.CharField()


class CommentForm(forms.Form):
    author_id = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

