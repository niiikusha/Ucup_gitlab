# from typing import Optional
# from ...models import Entity
# from django.db.models import Q
# from django.db.models.query import QuerySet


# class EntityLogic:
#     @staticmethod
#     def process_entity(msg: dict):
#         """
#             Обрабатывает продукт из топика "queuing.directory.internalCompanies"
#         """
#         try:
#             entity = Entity.objects.get(entity_id=msg['code'])
#             entity.name= msg['short_name']
#             entity.urastic_name = msg['name']
#             entity.rec_id = msg['name']
#             entity.director_name = msg['director_name']
#             entity.bank_bink = msg['bank_code']
#             entity.bank_name = msg['bank_name']
#             company_bank_account
#             entity.bank_name = msg['company_bank_account']


#             entity.save()
#         except entityment.DoesNotExist:
#            entityment.objects.create(product_key=msg['product_key'], external_code=msg['external_code'],type_entity = msg['type_entity'] )


#         {
# 	"name": "ООО \"ЕвроЛогистик\"",
# 	"short_name": "ООО \"ЕвроЛогистик\"",
# 	"code": "LEL",
# 	"rec_id": "5637680076",
# 	"director_name": "Федоров Дмитрий Сергеевич",
# 	"bank_code": "046902606",
# 	"bank_name": "ТОМСКОЕ ОТДЕЛЕНИЕ N8616 ПАО СБЕРБАНК",
# 	"company_bank_account": "40702810564000000939",
# 	"corr_bank_account": "30101810800000000606",
# 	"ogrn": "1217000008378"
# }