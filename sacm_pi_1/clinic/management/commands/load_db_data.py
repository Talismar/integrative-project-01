from django.core.management import call_command
from django.core.management.base import BaseCommand

from sacm_pi_1.users.models import CustomUser


class Command(BaseCommand):
    help = "Load db data"

    def handle(self, *args, **options):
        self.stdout.write("Migrating database...")
        call_command("migrate")

        if not CustomUser.objects.exists():
            call_command("populate_clinic_models")
            call_command("populate_users")
