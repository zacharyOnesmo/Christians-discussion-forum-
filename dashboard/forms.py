from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ClaimInputForm(forms.Form):
    claim = forms.CharField(
        label="Dai au madai",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Mfano: 666 ni chip ya ubongo",
                "class": "form-control",
            }
        ),
        max_length=500,
    )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, lang="sw", **kwargs):
        super().__init__(*args, **kwargs)
        if lang == "sw":
            self.fields["username"].label = "Jina la mtumiaji"
            self.fields["password"].label = "Nywila"
        else:
            self.fields["username"].label = "Username"
            self.fields["password"].label = "Password"


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, lang="sw", **kwargs):
        super().__init__(*args, **kwargs)
        if lang == "sw":
            self.fields["username"].label = "Jina la mtumiaji"
            self.fields["email"].label = "Barua pepe"
            self.fields["password1"].label = "Nywila"
            self.fields["password2"].label = "Rudia nywila"
        else:
            self.fields["username"].label = "Username"
            self.fields["email"].label = "Email"
            self.fields["password1"].label = "Password"
            self.fields["password2"].label = "Repeat password"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
