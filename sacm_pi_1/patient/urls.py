from django.urls import path
from .views import *

app_name = 'patient'
urlpatterns = [
    path('home/', home, name="home"),
    path('agenda/01/', agenda, name="agenda"),
    path('sobre/', AboutPageView.as_view(), name="sobre"),
    path('novo/agendamento/', novo_agendamento, name="novo_agendamento"),
    path('atualizar/agendamento/<int:pk>', atualizar_agendamento, name="atualizar_agendamento"),
    path('configuracao/usuario/', configUserADM, name="configuracao_usuario"),
    path('delete/photo/', delete_photo, name="delete_photo"),
]
