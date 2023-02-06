from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from sacm_pi_1.patient.models import Patient
from sacm_pi_1.clinic.models import Schedule
from sacm_pi_1.users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class PatientForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ["name", "email", "cpf", "username", "phone_number", "birth_date", "gender", "password1", "password2"]
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "cpf": "CPF",
            "username": "Matrícula",
            "phone_number": "Telefone",
            "birth_date": "Data de nascimento",
        }
        widgets = {
            "name": forms.TextInput(
                attrs= {
                    "placeholder": "Digite o nome do paciente...",
                }
            ),
            "email": forms.EmailInput(
                attrs= {
                    "placeholder": "Digite o email do paciente...",
                    "autocomplete": True
                }
            ),
            "cpf": forms.TextInput(
                attrs= {
                    "placeholder": "Digite um CPF no formato: XXX.XXX.XXX-XX",
                    "pattern": "\d{3}\.\d{3}\.\d{3}-\d{2}"
                }
            ),
            "username": forms.TextInput(
                attrs= {
                    "placeholder": "Digite a matrícula do paciente...",
                    "autocomplete": True
                }
            ),
            "phone_number": forms.TextInput(
                attrs= {"placeholder": "Digite um telefone no formato: (XX) X.XXXX-XXXX",
                # "pattern": "[7-9]{1}[0-9]{9}"
                }
            ),
            "birth_date": DateInput(),
            "gender": forms.RadioSelect()
        }

class CreateScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["speciality", "date", "hour", "description"]
        labels = {
            "speciality": "Especialidade:",
            "date": "Data:",
            "hour": "Hora:",
            "description": "Descrição",
        }
        widgets = {
            "hour": TimeInput(),
            "date": DateInput(format='%Y-%m-%d'),
            "description": forms.Textarea(
                attrs= {
                    "placeholder": "Digite uma descrição do seu problema..."
                }
            )
        }

class PatientChangeForm(UserChangeForm):
    password = None
    username = forms.CharField(help_text="", widget=forms.TextInput(attrs={'readonly': True}))
    gender = forms.ChoiceField(label="Sexo", disabled=True, choices=CustomUser.GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Patient
        fields = ['photo', 'name', 'email', 'phone_number', 'username', 'birth_date', 'cpf', 'gender']
        widgets = {
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

class PatientPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Senha antiga"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password1 = forms.CharField(
        label=_("Nova senha"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        required=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Repita a senha"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
