from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from config.settings.base import env
from sacm_pi_1.users.models import CustomUser


class Command(BaseCommand):
    help = "Create initial base users and groups"

    def handle(self, *args, **options):
        self._create_initial_groups()

        user = CustomUser.objects.all().exists()

        if user is not None:
            admin_group = Group.objects.get(name="Admin")

            user: CustomUser = CustomUser.objects.create_superuser(
                name="Talismar Fernandes Costa",
                email="talismar.una@gmail.com",
                phone_number="(84) 9.9970-2836",
                username="20211094040027",
                cpf="111.111.111-22",
                birth_date="1990-01-01",
                gender="Masculino",
            )

            user.groups.add(admin_group)
            user.set_password(env.str("ADMIN_USER_PASSWORD"))
            user.save()

        self.stdout.write(self.style.SUCCESS("Successfully populated users"))

    def _create_initial_groups(self):
        group_names = ["Admin", "Employee", "Patient"]

        for group_name in group_names:
            Group.objects.get_or_create(name=group_name)
