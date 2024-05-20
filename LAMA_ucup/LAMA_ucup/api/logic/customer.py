from typing import Optional
# from ...models import Customer
from django.db.models import Q
from django.db.models.query import QuerySet


# class CustomerLogic:
#     @staticmethod
#     def process_customer(msg: dict):
#         """
#             Обрабатывает продукт из топика "queuing.directory.internalCompanies"
#         """
#         try:
#             assort = Customer.objects.get(code = msg['code'])
#             assort.entity_id = msg['company_code']
#             assort.name = msg['name']
#             assort.organization_code = msg['organization_code']
#             assort.save()
#         except Customer.DoesNotExist:
#            Customer.objects.create(code=msg['code'], entity_id=msg['company_code'], name = msg['name'], organization_code = msg['organization_code'], )

# {
# 	"code": "НЕ-Кл000001075",
# 	"company_code": "nel",
# 	"name": "ООО \"Данлеко\"",
# 	"organization_code": "000114605"
# }