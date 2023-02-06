from django.db import models
from sacm_pi_1.users.models import CustomUser
from django.contrib.auth.models import Group

class Speciality(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class ScheduleStatus(models.Model):
    """
        Pendentes
        Concluidos
        Cancelados
    """

    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Schedule Status"

class Clinic(models.Model):
    """
        Um consultorio so pode ter um médico

    """

    name = models.CharField("Nome do consultório:", max_length=60)
    email = models.EmailField(verbose_name="E-mail do consultório:")
    phone_number = models.CharField(verbose_name="Telefone do consultório:", max_length=20, unique=True)
    address = models.CharField("Endereço do consultório", max_length=255, blank=False)
    speciality = models.ForeignKey(Speciality, verbose_name="Especialidade", on_delete=models.CASCADE)
    default_message_cancel = models.TextField("Mensagem padrão de cancelamento",blank=True)
    time_per_service = models.TimeField("Tempo por atendimento", blank=True, null=True)
    morning_start = models.TimeField("Inicio manhã", blank=True, null=True)
    morning_end = models.TimeField("Fim manhã", blank=True, null=True)
    afternoon_start = models.TimeField("Inicio tarde", blank=True, null=True)
    afternoon_end = models.TimeField("Fim tarde", blank=True, null=True)
    night_start = models.TimeField("Inicio noite", blank=True, null=True)
    night_end = models.TimeField("Fim noite", blank=True, null=True)

    def __str__(self):
        return self.name

class Employee(CustomUser):
    """
        Atendente
        Enfermeiros
        ...
    """
    """ Estou usando com blank e null True mas eu so cadastro um funcionanrio se existem o sistema """
    works_at = models.ForeignKey(Clinic, on_delete=models.CASCADE, blank=True, null=True)

    """
        groups - Employee

        groups = Group.objects.get(name="Employee")
    """

    def __str__(self):
        return self.username
    class Meta:
        db_table = 'Employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

class Doctor(Employee):
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    crm = models.CharField('CRM', max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

class Schedule(models.Model):

    matriculation = models.ForeignKey(CustomUser, verbose_name="Matricula", on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, verbose_name="Especialidade", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Data")
    hour = models.TimeField(verbose_name="Horário")
    description = models.TextField(verbose_name="Descrição")
    cancellation_message = models.TextField(default="", blank=True)
    scheduled_by = models.ForeignKey(CustomUser, related_name='scheduledBy_schedule_set', on_delete=models.CASCADE)

    """ Filtro por status de cancelado acess o cancellation_message """
    status = models.ForeignKey(ScheduleStatus, on_delete=models.CASCADE)
    id_system = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    # Update date
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.matriculation.username

