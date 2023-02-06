from django.urls import path
from sacm_pi_1.clinic.views import *
from sacm_pi_1.clinic.views_employee import *
from sacm_pi_1.clinic.views_schedule import *


app_name = 'clinic'
urlpatterns = [
    path('agenda/cancelar/agendamento/', CancelScheduleView.as_view(), name="cancel_schedule"),
    path('relatorio/pdf/', RelatorioPDFView.as_view(), name="relatorio_pdf"),
    path('novo/paciente/', PatientCretionView.as_view(), name="novo_paciente"),
    path('atualizar/agendamento/<int:pk>', UpdateScheduleView.as_view(), name="atualizar_agendamento"),
    path('calendario/', PageCalendarView.as_view(), name="calendario"),
    path('configuracao/sistema/', PageSystemSettingView.as_view(), name="configuracao_sistema"),
    path('configuracao/lista/usuarios/', ListUsersView.as_view(), name="lista_usuario"),
    path('configuracao/cadastrar/usuarios/', CreateUserEmployeeView.as_view(), name="cadastrar_usuario"),
    path('home/', ClinicHomeView.as_view(), name="home"),
    path('agenda/01/', ListScheduleView01.as_view(), name="agenda_01"),
    path('agenda/02/', ListScheduleView02.as_view(), name="agenda_02"),
    path('novo/agendamento/', ScheduleCreateView.as_view(), name="novo_agendamento"),
    path('configuracao/cadastrar/funcionario/', EmployeeSignupView.as_view(), name="cadastrar_funcionario"),
    path('configuracao/cadastrar/medico/', DoctorSignupView.as_view(), name="cadastrar_medico"),
    path('configuracao/usuario/', updateUser, name="configuracao_usuario"),
    path('configuracao/usuario/funcionario/', UpdateEmployeeView.as_view(), name="atualizar_funcionario"),
    path('configuracao/usuario/medico/', UpdateDoctorView.as_view(), name="atualizar_medico"),
    path("configuracao/detalhes/funcionario/<int:pk>", DetailEmployeeView.as_view(), name="detalhes_funcionario"),
    path('agendamento/mark/as/done/<int:pk>', mark_as_done, name="mark_as_done"),
    path('delete/employee/<int:pk>', delete_employee, name="delete_employee"),
    path('agenda/detalhe/<int:pk>', DetailScheduleView.as_view(), name="detalhe_agendamento"),
]
