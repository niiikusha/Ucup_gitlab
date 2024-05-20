from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Ku, Vendor, Entity
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status

class KuProcessing:
    _count = 0

    @staticmethod
    def create_ku(vendor_id, entity_id, period, date_start, status_ku, date_end=None, date_actual=None, graph_exists=None,
              description=None, contract=None, product_type=None, docu_account=None, docu_name=None, docu_number=None,
              docu_date=None, docu_subject=None, tax=None, exclude_return=None, negative_turnover=None,
              ku_type=None, pay_method=None):
        
        response_data = {}

        if Ku.objects.order_by('-ku_id').first():
            latest_ku = Ku.objects.order_by('-ku_id').first()
            ku_int = int(latest_ku.ku_id[2:])
            KuProcessing._count = ku_int + 1
        else:
            KuProcessing._count = 1

        ku_id = f'KY{KuProcessing._count:05}'
        date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
        date_start = datetime.strptime(date_start, '%Y-%m-%d').date()

        if not date_end or date_end > date_start + relativedelta(years=2):
            date_actual = date_start + relativedelta(years=2)

        if date_end and date_end < date_start:
            raise ValidationError("Дата окончания не должна быть раньше даты начала")
        
        vendor = Vendor.objects.get(vendor_id=vendor_id)
        entity = Entity.objects.get(entity_id=entity_id)

        ku = Ku.objects.create(
            ku_id=ku_id,
            vendor_id=vendor,
            entity_id=entity,
            period=period,
            date_start=date_start,
            date_end=date_end,
            status=status_ku,
            date_actual=date_actual,
            graph_exists=graph_exists,
            description=description,
            contract=contract,
            product_type=product_type,
            docu_account=docu_account,
            docu_name=docu_name,
            docu_number=docu_number,
            docu_date=docu_date,
            docu_subject=docu_subject,
            tax=tax,
            exclude_return=exclude_return,
            negative_turnover=negative_turnover,
            ku_type=ku_type,
            pay_method=pay_method
        )
        ku.save()

        response_data['ku_id'] = ku.ku_id
        response_data['status'] = 'true'

        return JsonResponse(response_data, status=status.HTTP_200_OK)
        