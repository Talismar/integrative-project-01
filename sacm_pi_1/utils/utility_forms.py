from django import forms
from sacm_pi_1.clinic.models import Clinic, Schedule
from datetime import datetime, time

# Customizing the default TimeInput and DateInput
class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'

TIME_PER_SERVICE = Clinic.objects.get(pk=1).time_per_service
MORNING_START = Clinic.objects.get(pk=1).morning_start
MORNING_END = Clinic.objects.get(pk=1).morning_end
AFTERNOON_START = Clinic.objects.get(pk=1).afternoon_start
AFTERNOON_END = Clinic.objects.get(pk=1).afternoon_end
NIGHT_START = Clinic.objects.get(pk=1).night_start
NIGHT_END = Clinic.objects.get(pk=1).night_end

def DATE_CHOICES(data=datetime.now().date()):
    return data

def TIME_CHOICES(*args, data=datetime.now().date()):
    CHOICES = []

    if len(args) > 2:
        data = datetime(int(args[0]), int(args[1]), int(args[2]))

    if MORNING_START and MORNING_END:
        filters = []

        for i in Schedule.objects.filter(date=data, hour__range=(MORNING_START, MORNING_END)):
            filters.append(i.hour)

        for i in range(MORNING_START.hour, MORNING_END.hour + TIME_PER_SERVICE.hour, TIME_PER_SERVICE.hour):
            i = time(i)
            if i not in filters:
                CHOICES.append((i, i))

    if AFTERNOON_START and AFTERNOON_END:
        filters = []

        for i in Schedule.objects.filter(date=data, hour__range=(AFTERNOON_START, AFTERNOON_END)):
            filters.append(i.hour)

        for i in range(AFTERNOON_START.hour, AFTERNOON_END.hour + TIME_PER_SERVICE.hour, TIME_PER_SERVICE.hour):
            i = time(i)
            if i not in filters:
                CHOICES.append((i, i))

    if NIGHT_START and NIGHT_END:
        filters = []

        for i in Schedule.objects.filter(date=data, hour__range=(NIGHT_START, NIGHT_END)):
            filters.append(i.hour)

        for i in range(NIGHT_START.hour, NIGHT_END.hour + TIME_PER_SERVICE.hour, TIME_PER_SERVICE.hour):
            i = time(i)
            if i not in filters:
                CHOICES.append((i, i))

    return CHOICES

"""
    1

    7 - 12
    14 - 17

"""
