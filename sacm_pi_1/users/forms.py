from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


CustomUser = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserCreationForm(UserCreationForm):


    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = "__all__"


###########################################

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'name', 'photo','birth_date', 'email', 'course', 'password1', 'password2']
#         widgets = {
#             'birth_date': forms.DateInput(attrs={'type': 'date'}),
#         }

# class CustomUserChangeForm(UserChangeForm):
#     password = None
#     username = forms.CharField(help_text="", widget=forms.TextInput(attrs={'readonly': True}))

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'name', 'photo', 'birth_date', 'email', 'course']
#         widgets = {
#             'birth_date': forms.DateInput(attrs={'type': 'date'}),
#         }

# class CustomPasswordChangeForm(PasswordChangeForm):
#     old_password = forms.CharField(
#         label=_("Old password"),
#         strip=False,
#         required=False,
#         widget=forms.PasswordInput(
#             attrs={"autocomplete": "current-password", "autofocus": True}
#         ),
#     )
#     new_password1 = forms.CharField(
#         label=_("New password"),
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#         strip=False,
#         required=False,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     new_password2 = forms.CharField(
#         label=_("New password confirmation"),
#         strip=False,
#         required=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#     )
