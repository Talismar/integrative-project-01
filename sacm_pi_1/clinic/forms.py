from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from .models import *
from django.contrib.auth import get_user_model
from utils.utility_forms import DATE_CHOICES, TIME_CHOICES, TimeInput, DateInput
from datetime import datetime as dt

CustomUser = get_user_model()

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = "__all__"

class UserChangeEmployeeForm(forms.ModelForm):
    gender = forms.ChoiceField(label="Sexo", disabled=True, choices=CustomUser.GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = CustomUser
        fields = ['photo', 'name', 'email', 'phone_number', 'username', 'birth_date', 'cpf', 'gender']
        labels = {
            "name": "Nome",
            "email": "Email",
            "phone_number": "Telefone",
            "username": "Matrícula",
        }
        widgets = {
            "photo": forms.FileInput(attrs={
                "class": "custom-file-input",
            }),
            "name": forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'input-text'}),
            "email": forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-text'}),
            "phone_number": forms.TextInput(attrs={'placeholder': 'Telefone', 'class': 'input-text'}),
            "username": forms.TextInput(attrs={'placeholder': 'Matrícula', 'class': 'input-text'}),
            "birth_date": DateInput(attrs={'placeholder': 'Data de nascimento', 'class': 'input-date'}, format='%Y-%m-%d'),
            "cpf": forms.TextInput(attrs={'placeholder': 'CPF', 'class': 'input-text'}),
        }

class UserEmployeeForm(UserCreationForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha', 'class': 'input-text'
    }))
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar senha', 'class': 'input-text'
    }))
    gender = forms.ChoiceField(label="Sexo", choices=CustomUser.GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = CustomUser
        fields = ['photo', 'name', 'email', 'phone_number', 'username', 'birth_date', 'cpf', 'gender', 'password1', 'password2']
        labels = {
            "name": "Nome",
            "email": "Email",
            "phone_number": "Telefone",
            "username": "Matrícula",
        }
        widgets = {
            "photo": forms.FileInput(),
            "name": forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'input-text'}),
            "email": forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-text'}),
            "phone_number": forms.TextInput(attrs={'placeholder': 'Telefone', 'class': 'input-text'}),
            "username": forms.TextInput(attrs={'placeholder': 'Matrícula', 'class': 'input-text'}),
            "birth_date": DateInput(attrs={'placeholder': 'Data de nascimento', 'class': 'input-date'}),
            "cpf": forms.TextInput(attrs={'placeholder': 'CPF', 'class': 'input-text'}),
        }

class UpdateScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["date", "hour", "description"]
        labels = {
            "date": "Data:",
            "hour": "Hora:",
            "description": "Descrição",
        }
        widgets = {
            "hour": TimeInput(),
            "date": DateInput(format='%Y-%m-%d')
        }

class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = "__all__"
        widgets = {
            "speciality": forms.Select(attrs={
                "hidden": True,
            }),
            "id_system": forms.Select(attrs={
                "hidden": True,
            }),
            "status": forms.Select(attrs={
                "hidden": True,
            }),
            "scheduled_by": forms.Select(attrs={
                "hidden": True,
            }),
            "matriculation": forms.Select(attrs={
                "hidden": True,
            })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.patient = None

        try:
            self.patient = kwargs.pop("patient")
        except:
            pass

        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['speciality'].initial = Speciality.objects.get(pk=1)
        self.fields['id_system'].initial = Clinic.objects.get(pk=1)
        self.fields['status'].initial = ScheduleStatus.objects.get(name="Pendente")
        self.fields['scheduled_by'].initial = self.request.user

        """ Quando usuario clicar em novo agendamento e veio do calendario """
        # try:
        #     if self.request.META['HTTP_REFERER'].split("?")[1].split("=")[0] == 'date':
        #         self.fields['date'].initial = self.request.META['HTTP_REFERER'].split("?")[1].split('=')[1]
        # except:
        #     pass


        if self.request.GET.get('new_schedule'):
            self.fields['date'].initial = self.request.GET.get('new_schedule')

            date = self.request.GET.get('new_schedule').split("-")
            self.fields['hour'] = forms.TimeField(widget=forms.Select(choices=TIME_CHOICES(*date)))

        else:
            try:
                if self.request.META['HTTP_REFERER'].split("?")[1].split('=')[0] == 'new_schedule':
                    self.fields['date'].initial = self.request.META['HTTP_REFERER'].split("?")[1].split('=')[1]

                    date = self.request.META['HTTP_REFERER'].split("?")[1].split('=')[1].split('-')
                    self.fields['hour'] = forms.TimeField(widget=forms.Select(choices=TIME_CHOICES(*date)))
            except:
                print("Error in ScheduleForm")

        if self.patient:
            self.fields['matriculation'].initial = self.patient

class ChangeScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'hour', 'description']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ChangeScheduleForm, self).__init__(*args, **kwargs)

        # print(self.instance.date)
        if self.request.GET.get('selected_date'):

            self.fields['date'].initial = self.request.GET.get('selected_date')

            date = self.request.GET.get('selected_date').split("-")
            self.fields['hour'] = forms.TimeField(widget=forms.Select(choices=TIME_CHOICES(*date)))
        else:
            self.fields['hour'] = forms.TimeField(widget=forms.Select(choices=[(self.instance.hour, self.instance.hour)] + TIME_CHOICES(data=self.instance.date)))

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = "__all__"
        widgets = {
            "time_per_service": TimeInput(format='%H:%M'),
            "morning_start": TimeInput(),
            "morning_end": TimeInput(),
            "afternoon_start": TimeInput(),
            "afternoon_end": TimeInput(),
            "night_start": TimeInput(),
            "night_end": TimeInput(),
        }

class EmployeeCreationForm(UserCreationForm):
    gender = forms.ChoiceField(label="Sexo", choices=CustomUser.GENDER_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Employee
        fields = ['works_at', 'photo', 'name', 'phone_number', 'email', 'username', 'cpf', 'birth_date', 'gender', 'password1', 'password2']
        widgets = {
            "photo": forms.FileInput(),
            "name": forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'input-text'}),
            "email": forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-text'}),
            "phone_number": forms.TextInput(attrs={'placeholder': 'Telefone', 'class': 'input-text'}),
            "username": forms.TextInput(attrs={'placeholder': 'Matrícula', 'class': 'input-text'}),
            "birth_date": DateInput(attrs={'placeholder': 'Data de nascimento', 'class': 'input-date'}),
            "cpf": forms.TextInput(attrs={'placeholder': 'CPF', 'class': 'input-text'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'input-text'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'input-text'
        })

class DoctorCreationForm(EmployeeCreationForm):

    class Meta(EmployeeCreationForm.Meta):
        model = Doctor
        fields = EmployeeCreationForm.Meta.fields + ['crm', 'speciality']
        widgets = {
            'speciality': forms.Select(attrs= {
                "class": "select-primary"
            }
            ),
            "birth_date": DateInput(attrs={'placeholder': 'Data de nascimento', 'class': 'input-date'}),
        }

    def __init__(self, *args, **kwargs):
        super(DoctorCreationForm, self).__init__(*args, **kwargs)
        self.fields['crm'].widget = forms.TextInput(
            attrs={
                'class': 'input-text',
            }
        )
        self.fields['speciality'].widget.attrs['class'] = 'select-primary'

class EmployeeChangeForm(UserChangeForm):
    password = None
    username = forms.CharField(help_text="", widget=forms.TextInput(attrs={'readonly': True}))
    gender = forms.ChoiceField(label="Sexo", disabled=True, choices=CustomUser.GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Employee
        fields = ['photo', 'name', 'email', 'phone_number', 'username', 'birth_date', 'cpf', 'gender']
        widgets = {
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

class DoctorChangeForm(EmployeeChangeForm):
    class Meta(EmployeeChangeForm.Meta):
        model = Doctor
        fields = EmployeeChangeForm.Meta.fields + ['crm', 'speciality']

    def __init__(self, *args, **kwargs):
        super(DoctorChangeForm, self).__init__(*args, **kwargs)
        self.fields['crm'].widget = forms.TextInput(
            attrs={
                'class': 'input-text',
            }
        )
        self.fields['speciality'].widget.attrs['class'] = 'select-primary'
        self.fields['speciality'].initial = self.instance.employee.doctor.speciality
        self.fields['crm'].initial = self.instance.employee.doctor.crm

class EmployeePasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Senha antiga"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password1 = forms.CharField(
        label=_("Novo senha"),
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


