from datetime import datetime, date
from sacm_pi_1.clinic.models import Schedule, ScheduleStatus

class SCHEDULING_FILTERS:

    def TODAY_CANCELED(self):
        return Schedule.objects.filter(status=ScheduleStatus.objects.get(name="Cancelado"), date=date.today()).count()

    def TODAY_COMPLETED(self):
        return Schedule.objects.filter(status=ScheduleStatus.objects.get(name="Concluído"), date=date.today()).count()

    def TODAY_PENDING(self):
        return Schedule.objects.filter(status=ScheduleStatus.objects.get(name="Pendente"), date=date.today()).count()

    def TODAY_TOTAL(self):
        return Schedule.objects.filter(date=datetime.now().date()).count()

