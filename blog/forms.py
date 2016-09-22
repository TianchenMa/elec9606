from django import forms


IS_PRIVATE = [
    (True, True),
    (False, False)
]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.PasswordInput()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    password = forms.PasswordInput()


class ImageUploadForm(forms.Form):
    profile = forms.ImageField()


class BlogForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    private = forms.ChoiceField(choices=IS_PRIVATE)


class ForwardForm(forms.Form):
    fwdcontent = forms.CharField(max_length=100)
    fwdprivate = forms.CharField()


class CommentForm(forms.Form):
    author_id = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

