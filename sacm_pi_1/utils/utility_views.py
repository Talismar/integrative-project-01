from datetime import date, datetime

from sacm_pi_1.clinic.models import Schedule, ScheduleStatus


class SCHEDULING_FILTERS:

    def TODAY_CANCELED(self):
        return Schedule.objects.filter(
            status=ScheduleStatus.objects.get_or_create(name="Cancelado")[0],
            date=date.today(),
        ).count()

    def TODAY_COMPLETED(self):
        return Schedule.objects.filter(
            status=ScheduleStatus.objects.get_or_create(name="Concluído")[0],
            date=date.today(),
        ).count()

    def TODAY_PENDING(self):
        return Schedule.objects.filter(
            status=ScheduleStatus.objects.get_or_create(name="Pendente")[0],
            date=date.today(),
        ).count()

    def TODAY_TOTAL(self):
        return Schedule.objects.filter(date=datetime.now().date()).count()
