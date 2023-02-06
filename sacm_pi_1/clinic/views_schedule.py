from django.http import HttpRequest, HttpResponse
from traitlets import Any
from .imports import *
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View, TemplateView, DetailView, UpdateView, CreateView
from utils.utility_views import SCHEDULING_FILTERS
from braces.views import GroupRequiredMixin
from django.contrib import messages

class MyMixin(GroupRequiredMixin):

    def check_membership(self, group):

        if self.request.user.groups.all()[0].name in group:
            return True
        else:
            messages.error(self.request, 'Você não possui acesso a essa área do sistema.')
            return False


class ListScheduleView01(MyMixin, LoginRequiredMixin, ListView):
    template_name = "clinic/agenda_01.html"
    extra_context = {
        "diary": True,
    }
    model = Schedule
    group_required = [u'Admin', u'Employee']
    paginate_by = 7
    ordering = ["pk"]

    def __init__(self, *args, **kwargs):
        self._date = ""
        super().__init__(*args, **kwargs)

    def get_queryset(self,):
        self.search = self.request.GET.get('search')

        if not self.request.GET.get('new_schedule'):
            self.extra_context['day'] = datetime.date.today().day
            self.extra_context['name_month'] = month[datetime.date.today().month]
            self.extra_context['month'] = datetime.date.today().month
            self.extra_context['year'] = datetime.date.today().year

            if self.search:
                matriculation = CustomUser.objects.filter(username__icontains=self.search)

                # print(matriculation[0].pk)

                return super().get_queryset().filter(matriculation=matriculation[0].pk)

            else:
                return super().get_queryset().filter(date=datetime.date.today())

        else:
            self.extra_context['day'] = self.request.GET.get('new_schedule').split("-")[2]
            self.extra_context['month'] = self.request.GET.get('new_schedule').split("-")[1]
            self.extra_context['year'] = self.request.GET.get('new_schedule').split("-")[0]
            self.extra_context['name_month'] = month[int(self.request.GET.get('new_schedule').split("-")[1])]

            if self.request.GET.get('search'):
                print("Searching")

            return super().get_queryset().filter(date=self.request.GET.get('new_schedule'))

class ListScheduleView02(ListScheduleView01):
    template_name = "clinic/agenda_02.html"

class ScheduleCreateView(MyMixin, LoginRequiredMixin, CreateView):
    template_name = "clinic/novo_agendamento.html"
    form_class = ScheduleForm
    success_url = reverse_lazy('clinic:agenda_01')
    group_required = [u"Admin", u"Employee"]

    def __init__(self, *args, **kwargs):
        super(ScheduleCreateView, self).__init__(*args, **kwargs)
        self.URL_WITH_DATE = ""

    def get(self, request, *args: str, **kwargs):

        if request.GET.get('new_schedule'):
            self.extra_context = { 'new_schedule': request.GET.get('new_schedule') }

        try:
            if request.META['HTTP_REFERER'].split("?")[1].split("=")[0] == 'new_schedule':
                self.URL_WITH_DATE = request.META['HTTP_REFERER'].split("?")[1].split("=")[1]
                self.extra_context = { 'new_schedule': self.URL_WITH_DATE }

        except IndexError:
            pass

        """ Mudar o model de busca tem que ser o Patient model """
        if request.GET.get('search_patient'):
            try:
                patient = CustomUser.objects.get(username=request.GET.get('search_patient'))
                self.extra_context = {
                    "patient": patient
                }

            except CustomUser.DoesNotExist:
                """ Devo abrir o modal para informar que devo ir pra pagina de cadastro de patient
                    ou ir direto pra ela
                """
                print('Error does not exist patient')
                self.extra_context = {
                    "patient_does_not_exist": True, # Modal
                    "new_schedule": request.GET.get("new_schedule")
                }
                print(request.GET.get("new_schedule"))
            # return redirect('novoclinic:_paciente')

        return super().get(request, *args, **kwargs)

    def form_valid(self, request, form) -> HttpResponse:
        self.object = form.save()

        url_ = '?new_schedule=' + request.GET.get('new_schedule')
        messages.success(request, 'Novo agendamento cadastrado com sucesso')

        return HttpResponseRedirect('/clinic/agenda/01/'+url_)

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        form = self.get_form()
        self.object=None
        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    # PassRequestToFormViewMixin
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        try:
            kwargs['patient'] = self.extra_context['patient']
        except:
            pass

        return kwargs

class UpdateScheduleView(MyMixin, LoginRequiredMixin, UpdateView):
    template_name = "clinic/atualizar_agendamento.html"
    model = Schedule
    form_class = ChangeScheduleForm
    group_required = [u'Admin', u'Employee']
    success_url = reverse_lazy('clinic:agenda_01')

    # PassRequestToFormViewMixin
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        print(kwargs)
        try:
            kwargs['patient'] = self.extra_context['patient']
        except:
            pass

        return kwargs

class DetailScheduleView(MyMixin, LoginRequiredMixin, DetailView):
    template_name = "clinic/detalhe_paciente.html"
    group_required = [u'Admin', u'Employee']
    model = Schedule
    extra_context = {
        "diary": True
    }
    context_object_name = 'data'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        self.extra_context.update({'phone_number': Schedule.objects.get(pk=kwargs['pk']).matriculation.phone_number})

        return super().get(request, *args, **kwargs)

class CancelScheduleView(LoginRequiredMixin, View):
    model_shedule = Schedule
    model_shedule_status = ScheduleStatus

    def get(self, request):
        cancelled_status = self.model_shedule_status.objects.get(name="Cancelado")


        if request.GET.get('_pk_'):
            schedule = self.model_shedule.objects.get(pk=request.GET.get('_pk_'))
            schedule.status = cancelled_status
            schedule.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def post(self, request, *args, **kwargs):
        cancelled_status = self.model_shedule_status.objects.get(name="Cancelado")

        if request.POST.get('message_cancellation'):
            schedule = self.model_shedule.objects.get(pk=request.POST.get('pk'))
            schedule.status = cancelled_status
            schedule.cancellation_message = request.POST.get('message_cancellation')
            schedule.save()
        else:
            schedule = self.model_shedule.objects.get(pk=request.POST.get('pk'))
            schedule.status = cancelled_status
            schedule.cancellation_message = Clinic.objects.get(pk=1).default_message_cancel
            schedule.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

