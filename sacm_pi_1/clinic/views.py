from django.http import HttpRequest, HttpResponse
from traitlets import Any
from .imports import *
from django.views.generic import TemplateView, DetailView, CreateView
from utils.utility_views import SCHEDULING_FILTERS
from datetime import datetime as dt
from django.contrib import messages
from braces.views import GroupRequiredMixin
from .views_schedule import MyMixin

class ClinicHomeView(MyMixin, LoginRequiredMixin, TemplateView, SCHEDULING_FILTERS):
    template_name = 'clinic/home.html'
    group_required = [u'Admin', u'Employee']

    def get_context_data(self, **kwargs):
        context = {
            "home_item": [
                {"title": "Agendamentos de hoje", "icon": "stethoscope", "count": self.TODAY_TOTAL()},
                {"title": "Concluídos", "icon": "check_square", "count": self.TODAY_COMPLETED()},
                {"title": "Pendentes", "icon": "hand_palm", "count": self.TODAY_PENDING()},
            ],
            "home": True
        }

        return context

class PageSystemSettingView(MyMixin, LoginRequiredMixin, DetailView):
    template_name = "clinic/config_sistema.html"
    group_required = [u'Admin', u'Employee']
    extra_context = {
        "setting": True,
    }
    form_class = ClinicForm
    context_object_name = "form"

    def get_object(self, queryset=None) -> models.Model:
        admin_logged_in = self.request.user.pk

        try:
            instance = Clinic.objects.get(pk=admin_logged_in)
        except:
            return HttpResponse("Sem permission")

        return self.form_class(instance=instance)

class ListUsersView(MyMixin, LoginRequiredMixin, ListView):
    template_name = "clinic/lista_funcionarios.html"
    group_required = [u'Admin', u'Employee']
    extra_context = {
        "setting": True
    }
    model = Employee
    paginate_by = 7
    ordering = ["pk"]

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        try:
            """ Primeiro funcionário do sistem deve ser o médico """
            doctor = Doctor.objects.all()[self.request.user.pk-1]

        except IndexError:
            self.extra_context.update({'there_is_no_doctor': True})

        return super().get(request, *args, **kwargs)

class CreateUserEmployeeView(MyMixin, LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    user_form_class = UserEmployeeForm
    group_required = [u'Admin', u'Employee']
    template_name = "pages_clinic/configuracao/04_cadastrar_usuario.html"
    success_url = reverse_lazy('lista_usuario_consultorio')

    def get(self, request):
        profile_form = self.form_class()
        user_form = self.user_form_class()

        context = {
            'profile_form': profile_form,
            'user_form': user_form,
            "setting": True
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile_form = self.form_class(request.POST)
        user_form = self.user_form_class(request.POST, request.FILES)

        if all([profile_form.is_valid(), user_form.is_valid()]):
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            group = Group.objects.get(name="Employee")
            user = Employee.objects.get(user__username=request.POST.get('username'))

            user.user.groups.add(group)
            user.save()

        else:
            # print("ERROR: Failed to save profile")
            return render(request, self.template_name, {'profile_form': profile_form, 'user_form': user_form})

        return HttpResponseRedirect(self.success_url)

class RelatorioPDFView(MyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'clinic/relatorio.html'
    group_required = [u'Admin', u'Employee']

    def get(self, request, *args: Any, **kwargs: Any):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        with_name_patient = request.GET.get('with_name')
        with_hour_schedule = request.GET.get('with_hour')
        with_status = request.GET.get('with_status')

        object_filter = Schedule.objects.filter(date__range=[start_date, end_date])

        status = request.GET.get('status')
        if with_status and status:

            print(status)

            if status == 'attended':
                status_attended = ScheduleStatus.objects.get(name="Concluído")
                object_filter = Schedule.objects.filter(status=status_attended,  date__range=[start_date, end_date])
            elif status == 'unanswered':
                status_unanswered = ScheduleStatus.objects.get(name="Pendente")
                object_filter = Schedule.objects.filter(status=status_unanswered,  date__range=[start_date, end_date])

        self.extra_context = {
            'object_filter': object_filter,
            'period_filter': [start_date, end_date],
            'with_name_patient': with_name_patient,
            'with_hour_schedule': with_hour_schedule,
            'with_status': status
        }

        return super().get(request, *args, **kwargs)

class PageCalendarView(MyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'clinic/calendar.html'
    group_required = [u'Admin', u'Employee']

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            return redirect('/clinic/relatorio/pdf/?' + request.get_full_path_info().split('?')[1])

        kwargs['month_year'] = request.GET.get('month_year')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = Calendar()
        days = {
            "date": [],
            "data": []
        }

        get_month_year = context['month_year']

        if get_month_year:

            for day in obj.itermonthdates(int(get_month_year.split('-')[0]), int(get_month_year.split('-')[1])):

                if day.day >= 1 and day.month == int(get_month_year.split('-')[1]):
                    days["date"].append({
                        "another_month": False,
                        "current_month": day
                    })
                else:
                    days["date"].append({
                        "another_month": day,
                        "current_month": False
                    })

                days["data"].append({
                    "concluido": Schedule.objects.filter(date=day, status=ScheduleStatus.objects.get(name="Concluído")).count(),
                    "pendente": Schedule.objects.filter(date=day, status=ScheduleStatus.objects.get(name="Pendente")).count(),
                    "is_weekend": True if day.weekday() in [5,6] else False
                })

        else:
            for day in obj.itermonthdates(datetime.date.today().year, datetime.date.today().month):

                if day.day >= 1 and day.month == datetime.date.today().month:
                    days["date"].append({
                        "another_month": False,
                        "current_month": day
                    })
                else:
                    days["date"].append({
                        "another_month": day,
                        "current_month": False
                    })

                days["data"].append({
                    "concluido": Schedule.objects.filter(date=day, status=ScheduleStatus.objects.get(name="Concluído")).count(),
                    "pendente": Schedule.objects.filter(date=day, status=ScheduleStatus.objects.get(name="Pendente")).count(),
                    "is_weekend": True if day.weekday() in [5,6] else False
                })

        context["calendar"] = True
        context["days"] = zip(days["date"], days["data"])
        context["today"] = datetime.date.today()
        context["month_year"] = get_month_year if get_month_year else str(datetime.date.today())[:-3]

        return context

def mark_as_done(request, pk):
    mark = get_object_or_404(Schedule, pk=pk)

    instance_done = ScheduleStatus.objects.get(name="Concluído")

    mark.status = instance_done
    mark.save()

    return redirect(request.META['HTTP_REFERER'])

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()

    return redirect('lista_usuario')
