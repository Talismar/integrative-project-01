from django.http import HttpRequest, HttpResponse
from traitlets import Any
from .imports import *
from django.contrib.auth.forms import PasswordChangeForm
from sacm_pi_1.users.views import UserLoginView, UpdateProfileView
from sacm_pi_1.patient.forms import PatientForm
from django.views.generic import View, TemplateView, DetailView, UpdateView, CreateView
from utils.utility_views import SCHEDULING_FILTERS
from django.contrib import messages


class EmployeeSignupView(LoginRequiredMixin, UserLoginView):
    template_name = 'clinic/cadastrar_funcionario.html'
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('lista_usuario_consultorio')
    extra_context = {
        "form_title": "Novo Funcionário",
    }

    def form_valid(self, request, form):

        form = form.save(commit=False)

        form.works_at = Clinic.objects.get(pk=1)

        self.object = form.save()

        employee_group = Group.objects.get_or_create(name="Employee")
        Employee.objects.all().last().groups.add(employee_group[0])

        messages.success(request, 'Novo funcionario cadastrado com sucesso')

        return HttpResponseRedirect('/clinic/configuracao/lista/usuarios/')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        self.object=None
        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

class DoctorSignupView(EmployeeSignupView):
    form_class = DoctorCreationForm
    success_url = reverse_lazy('lista_usuario_consultorio')
    extra_context = {
        "form_title": "Cadastrar Médico"
    }

def updateUser(request):
    try:
        request.user.employee.doctor
        return redirect('clinic:atualizar_medico')
    except:
        return redirect('clinic:atualizar_funcionario')

class UpdateEmployeeView(LoginRequiredMixin, UpdateProfileView):
    template_name = 'clinic/perfil_usuario.html'
    form_class = EmployeeChangeForm
    password_form_class = EmployeePasswordChangeForm
    success_url = reverse_lazy('clinic:configuracao_usuario')


class UpdateDoctorView(UpdateEmployeeView):
    form_class = DoctorChangeForm


class PatientCretionView(LoginRequiredMixin, CreateView):
    template_name = "clinic/cadastrar_paciente.html"
    form_class = PatientForm
    extra_context = {
        "diary": True
    }

    def get_context_data(self, **kwargs):
        # if self.request.GET.get('search_patient'):
        #     kwargs.update({'username': self.request.GET.get('search_patient')})

        try:
            kwargs.update({'username': self.request.META['HTTP_REFERER'].split('search_patient=')[1]})
        except IndexError:
            pass # Não veio o parametro na url search_patient

        return super().get_context_data(**kwargs)

    def form_valid(self, request, form) -> HttpResponse:
        self.object = form.save()

        patient_group = Group.objects.get_or_create(name="Patient") # return (<Group: Patient>, False)
        self.object.groups.add(patient_group[0])

        url_ = '?new_schedule=' + request.GET.get('new_schedule') + '&search_patient=' + self.object.username
        messages.success(request, 'Novo paciente cadastrado com sucesso')
        return HttpResponseRedirect('/clinic/novo/agendamento/'+url_)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        self.object=None
        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        # print("try")
        return super().get(request, *args, **kwargs)

class DetailEmployeeView(LoginRequiredMixin, DetailView):
    template_name = 'clinic/detalhe_funcionario.html'
    # model = Employee
    success_url = reverse_lazy('lista_usuario_consultorio')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        try:
            Doctor.objects.get(pk=kwargs['pk'])
            self.model =Doctor
        except Doctor.DoesNotExist:
            self.model = Employee

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # self.model = Doctor
        # kwargs['object'].speciality
        try:
            self.model = Doctor
            kwargs['object'].speciality
            context['form'] = DoctorChangeForm(instance=kwargs['object'])
        except:
            context['form'] = EmployeeChangeForm(instance=kwargs['object'])

        context['password_form'] = EmployeePasswordChangeForm(user=kwargs['object'])

        return context
