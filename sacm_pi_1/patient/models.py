from typing import Iterable, Optional
from django.contrib.auth.models import Group
from django.db import models
from sacm_pi_1.users.models import CustomUser

class Patient(CustomUser):
    class Meta:
        pass
