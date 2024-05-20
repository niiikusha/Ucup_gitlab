from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import KuCustomer, Customer, Entity
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status

class KuCustomerProcessing:
    _count = 0

    @staticmethod
    def create_ku_customer(customer_id, entity_id, period, date_start, status_ku, date_end=None, date_actual=None, graph_exists=None,
              description=None, contract=None, docu_account=None, docu_number=None,
              docu_date=None, docu_subject=None, pay_method=None, pay_sum=None):
        
        response_data = {}

        if KuCustomer.objects.order_by('-ku_id').first():
            latest_ku = KuCustomer.objects.order_by('-ku_id').first()
            ku_int = int(latest_ku.ku_id[2:])
            KuCustomerProcessing._count = ku_int + 1
        else:
            KuCustomerProcessing._count = 1

        ku_id = f'KY{KuCustomerProcessing._count:05}'
        date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
        date_start = datetime.strptime(date_start, '%Y-%m-%d').date()

        if not date_end or date_end > date_start + relativedelta(years=2):
            date_actual = date_start + relativedelta(years=2)

        if date_end and date_end < date_start:
            raise ValidationError("Дата окончания не должна быть раньше даты начала")
        
        customer = Customer.objects.get(customer_id=customer_id)
        entity = Entity.objects.get(entity_id=entity_id)

        ku = KuCustomer.objects.create(
            ku_id=ku_id,
            customer_id=customer,
            entity_id=entity,
            period=period,
            date_start=date_start,
            date_end=date_end,
            status=status_ku,
            date_actual=date_actual,
            graph_exists=graph_exists,
            description=description,
            contract=contract,
            docu_account=docu_account,
            docu_number=docu_number,
            docu_date=docu_date,
            docu_subject=docu_subject,
            pay_method=pay_method,
            pay_sum=pay_sum
        )
        ku.save()

        response_data['ku_id'] = ku.ku_id
        response_data['status'] = 'true'

        return JsonResponse(response_data, status=status.HTTP_200_OK)