from datetime import time

from django.core.management.base import BaseCommand

from sacm_pi_1.clinic.models import Clinic, ScheduleStatus, Speciality


class Command(BaseCommand):
    help = "Create initial base clinic instances"

    def handle(self, *args, **options):
        self._create_initial_schedule_status()
        speciality = self._get_or_create_speciality()

        clinic = Clinic.objects.all().exists()

        if clinic is not None:
            Clinic.objects.create(
                name="IFRN - Centro médico",
                email="ifrncentromedico@gmail.com",
                phone_number="(84) 9.9999-9999",
                address="Rua josé joaquim duarte 111, centro, Pau dos Ferros-RN",
                speciality=speciality,
                default_message_cancel="Mensagem padrão de cancelamento",
                time_per_service=time(1),
                morning_start=time(7),
                morning_end=time(12),
                afternoon_start=time(13),
                afternoon_end=time(17),
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated clinic models"))

    def _get_or_create_speciality(self):
        speciality, _ = Speciality.objects.get_or_create(name="Medicina Geral")
        return speciality

    def _create_initial_schedule_status(self):
        schedule_status_names = ["Pendente", "Concluído", "Cancelado"]

        for schedule_status_name in schedule_status_names:
            ScheduleStatus.objects.get_or_create(name=schedule_status_name)
