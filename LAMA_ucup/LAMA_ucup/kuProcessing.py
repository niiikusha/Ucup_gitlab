from dateutil.relativedelta import relativedelta
from .models import Ku
from django.core.exceptions import ValidationError

class KuProcessing:
    _count = 0

    @staticmethod
    def create_ku(vendor_id, entity_id, period, date_start, status_ku, date_end=None, date_actual=None, percent=None, graph_exists=None):
    
        if Ku.objects.order_by('-ku_id').first():
            latest_ku = Ku.objects.order_by('-ku_id').first()
            ku_int = int(latest_ku.ku_id[2:])
            KuProcessing._count = ku_int + 1
        else:
            KuProcessing._count = 1

        ku_id = f'KY{KuProcessing._count:05}'

        if not date_end or date_end > date_start + relativedelta(years=2):
            date_actual = date_start + relativedelta(years=2)

        if date_end and date_end < date_start:
            raise ValidationError("Дата окончания не должна быть раньше даты начала")
        
        ku = Ku.objects.create(
            ku_id=ku_id,
            vendor_id=vendor_id,
            entity_id=entity_id,
            period=period,
            date_start=date_start,
            date_end=date_end,
            status=status_ku,
            date_actual=date_actual,
            percent=percent,
            graph_exists=graph_exists
        )

        ku.save()

        # instance.save()
        # return  instance