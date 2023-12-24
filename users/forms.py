from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from catalog.forms import StyleFormMixin
from users.models import User, Verify


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class VerifyForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Verify
        fields = ('verify_pass',)



