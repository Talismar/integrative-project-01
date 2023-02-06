from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from sacm_pi_1.clinic.models import Schedule, CustomUser, ScheduleStatus, Clinic, Speciality
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from utils.utility_forms import TIME_CHOICES
from .models import Patient
from .forms import CreateScheduleForm, PatientChangeForm, PatientPasswordChangeForm
from django import forms
from datetime import datetime as dt
from django.contrib import messages

class AboutPageView(TemplateView):
    template_name = 'patient/sobre.html'
    extra_context = {
        "about": True
    }

    def get(self, request, *args, **kwargs):
        kwargs.update({'notification': Schedule.objects.filter(matriculation=request.user.pk).order_by('id')})

        concluido = ScheduleStatus.objects.get(name="Concluído")
        kwargs.update({"notification_count": len(kwargs['notification']) - len(kwargs['notification'].filter(status= concluido))})
        return super().get(request, *args, **kwargs)

@login_required
def home(request):
    if not request.user.groups.filter(name='Patient').exists():
        messages.error(request, 'Você não possui acesso a essa área do sistema.')
        return redirect('users:login')

    notification = Schedule.objects.filter(matriculation=request.user.pk).order_by('id')
    concluido = ScheduleStatus.objects.get(name="Concluído")
    notification_count = len(notification) - len(notification.filter(status= concluido))

    days = Schedule.objects.filter(matriculation=request.user.pk).count()
    pendente = Schedule.objects.filter(
                                        matriculation=request.user.pk,
                                        status=ScheduleStatus.objects.get(name="Pendente")
                                      ).count()
    concluido = Schedule.objects.filter(
                                        matriculation=request.user.pk,
                                        status=ScheduleStatus.objects.get(name="Concluído")
                                       ).count()

    context = {
        "home_item": [
            {"title": "Últimos 30 dias", "icon": "stethoscope", "count": days},
            {"title": "Concluídos", "icon": "check_square", "count": concluido},
            {"title": "Pendentes", "icon": "hand_palm", "count": pendente},
        ],
        "home": True,
        "notification": notification,
        "notification_count": notification_count
    }
    # print('HEREEE...',request.user.groups.filter(name='Admin').exists())

    return render(request, "patient/home.html",context)

@login_required
def agenda(request):
    if not request.user.groups.filter(name='Patient').exists():
        messages.error(request, 'Você não possui acesso a essa área do sistema.')
        return redirect('users:login')

    list_schedule = Schedule.objects.filter(matriculation=request.user.pk).order_by('id')
    notification = list_schedule
    concluido = ScheduleStatus.objects.get(name="Concluído")
    notification_count = len(notification) - len(notification.filter(status= concluido))

    if request.GET.get('date'):
        list_schedule = Schedule.objects.filter(date=request.GET.get('date'), matriculation=request.user.pk)

    paginator = Paginator(list_schedule, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "diary": True,
        "list_schedule": page_obj,
        'page_obj': page_obj,
        'notification': notification,
        "notification_count": notification_count
    }

    return render(request, "patient/agenda.html", context)

@login_required
def novo_agendamento(request):
    if not request.user.groups.filter(name='Patient').exists():
        messages.error(request, 'Você não possui acesso a essa área do sistema.')
        return redirect('users:login')

    notification = Schedule.objects.filter(matriculation=request.user.pk).order_by('id')
    concluido = ScheduleStatus.objects.get(name="Concluído")
    notification_count = len(notification) - len(notification.filter(status= concluido))
    initial_data = {
        'date' : dt.today().strftime("%Y-%m-%d"),
    }

    form = CreateScheduleForm(initial=initial_data)
    form.fields['hour'] = forms.TimeField(widget=forms.Select(choices=TIME_CHOICES(data=dt(2023,1,16).date())))

    if request.method == 'GET' and request.GET.get('new_date'):
        print("New date")


    if request.method == "POST":
        form = CreateScheduleForm(request.POST)

        if form.is_valid():
            # print('Validated')
            form = form.save(commit=False)
            messages.success(request, 'Novo agendamento cadastrado com sucesso!')

            model = Schedule
            model.objects.create(
                matriculation=request.user,
                speciality=form.speciality,
                date=form.date,
                hour=form.hour,
                description=form.description,
                scheduled_by=CustomUser.objects.get(pk=request.user.pk),
                status = ScheduleStatus.objects.get(name="Pendente"),
                id_system=Clinic.objects.get(speciality=Speciality.objects.get(name="Clinico Geral"))
            )

            return redirect("patient:agenda")

    context = {
        "diary": True,
        "form": form,
        "notification": notification,
        "notification_count": notification_count
    }

    return render(request, "patient/novo_agendamento.html", context)

@login_required
def atualizar_agendamento(request, pk):
    if not request.user.groups.filter(name='Patient').exists():
        messages.error(request, 'Você não possui acesso a essa área do sistema.')
        return redirect('users:login')

    notification = Schedule.objects.filter(matriculation=request.user.pk).order_by('id')
    concluido = ScheduleStatus.objects.get(name="Concluído")
    notification_count = len(notification) - len(notification.filter(status= concluido))
    instance = get_object_or_404(Schedule, pk=pk)

    if request.method == "POST":
        form = CreateScheduleForm(request.POST, instance=instance)
        # form.get_context()['form'].fields['speciality'].initial = instance.speciality
        # print(form.get_context()['form'].fields['speciality'].widget)

        if form.is_valid():
            form.save()

            return redirect("patient:agenda")

    else:
        initial_data = {
            'date' : instance.date,
            'speciality' : instance.speciality
        }

        form = CreateScheduleForm(instance=instance, initial=initial_data)
        form.fields['hour'] = forms.TimeField(widget=forms.Select(choices=[((instance.hour), (instance.hour))] + TIME_CHOICES(data=instance.date)))
        form.fields['speciality'] = forms.ModelChoiceField(queryset = Speciality.objects.all())

    context = {
        "diary": True,
        "form": form,
        'notification': notification,
        'notification_count': notification_count
    }

    return render(request, "patient/atualizar_agendamento.html", context)

@login_required
def sobre_paciente(request):
    if not request.user.groups.filter(name='Patient').exists():
        messages.error(request, 'Você não possui acesso a essa área do sistema.')
        return redirect('users:login')

    notification = Schedule.objects.filter(matriculation=request.user.pk).order_by('id')
    concluido = ScheduleStatus.objects.get(name="Concluído")
    notification_count = len(notification) - len(notification.filter(status= concluido))

    return render(request, 'pages/sobre.html', {"about": True,
        "notification": notification, 'notification_count': notification_count})

@login_required
def configUserADM(request):
    if not request.user.groups.filter(name='Patient').exists():
        messages.error(request, 'Você não possui acesso a essa área do sistema.')
        return redirect('users:login')

    notification = Schedule.objects.filter(matriculation=request.user.pk).order_by('id')
    concluido = ScheduleStatus.objects.get(name="Concluído")
    notification_count = len(notification) - len(notification.filter(status= concluido))
    user = get_object_or_404(Patient, pk=request.user)

    form = PatientChangeForm(instance=user)
    password_form = PatientPasswordChangeForm(user=user)

    if request.method == 'POST':
        print(request.POST)
        form = PatientChangeForm(request.POST, request.FILES, instance=user)

        password_post = {
                            "old_password": request.POST.get("old_password"),
                            "new_password1": request.POST.get("new_password1"),
                            "new_password2": request.POST.get("new_password2")
                        }

        password_form = PatientPasswordChangeForm(user=user, data=password_post)
        print(password_form.is_valid())
        print(form.is_valid())

        if len(request.POST.get('old_password')) > 0 and  password_form.is_valid():
            password_form.save()
            messages.success(request, "Senha alterada com sucesso!")

        if len(request.POST.get('old_password')) > 0 and not password_form.is_valid():
            context = {
                "form": form,
                'password_form': password_form,
                "setting": True,
                "notification": notification,
                "notification_count": notification_count
            }

            return render(request,"patient/config_usuario.html", context)


        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizados com sucesso!")

            return redirect('patient:configuracao_usuario')



    context = {
        "form": form,
        'password_form': password_form,
        "setting": True,
        "notification": notification,
        "notification_count": notification_count
    }

    return render(request,"patient/config_usuario.html", context)

@login_required
def delete_photo(request):
    photo = get_object_or_404(Patient, pk=request.user)

    if photo.photo:
        photo.photo.delete()

    return redirect('patient:configuracao_usuario')
