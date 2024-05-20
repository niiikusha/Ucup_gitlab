from typing import Optional
from ...models import Assortment
from django.db.models import Q
from django.db.models.query import QuerySet


class AssortmentLogic:
    @staticmethod
    def process_assortment(msg: dict):
        """
            Обрабатывает продукт из топика "queuing.directory.internalCompanies"
        """
        try:
            assort = Assortment.objects.get(product_key=msg['product_key'])
            assort.external_code = msg['external_code']
            assort.type_assort = msg['type_assort']
            assort.save()
        except Assortment.DoesNotExist:
           Assortment.objects.create(product_key=msg['product_key'], external_code=msg['external_code'],type_assort = msg['type_assort'] )