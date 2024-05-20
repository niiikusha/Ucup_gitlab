from typing import Optional
from ...models import Vendor, Entity
from django.db.models import Q
from django.db.models.query import QuerySet


class VendorLogic:
#     @staticmethod
#     def get_list(vendor_id: Optional[int]) -> QuerySet:
#         condition = Q()
#         if vendor_id is not None:
#             condition |= Q(id=vendor_id)

#         condition.connector = Q.AND
#         return Vendor.objects.filter(condition)

    @staticmethod
    def process_vendor(msg: dict):
        """
            Обрабатывает компанию из топика "queuing.directory.internalCompanies"
        """
        try:
            vendor = Vendor.objects.get(vendor_id=msg['code'])
            vendor.name = msg.get('short_name', vendor.name)
            entity, _ = Entity.objects.get_or_create(entity_id=msg.get('company_code', ''))
            vendor.entity_id = entity
            # vendor.entity_id = msg.get('company_code', vendor.entity_id)
            vendor.urastic_name = msg.get('name', vendor.urastic_name)
            vendor.director_name = msg.get('director_name', vendor.director_name)
            if 'inn' in msg and 'kpp' in msg:
                vendor.inn_kpp = msg['inn'] + '/' + msg['kpp']
            #vendor.inn_kpp = msg.get('inn', '') + '/' + msg.get('kpp', '')
            vendor.urastic_adress = msg.get('address', vendor.urastic_adress)
            vendor.bank_bik = msg.get('bank_code', vendor.bank_bik)
            vendor.organization_code = msg.get('organization_code', vendor.organization_code)
            vendor.dir_party = msg.get('rec_id', vendor.dir_party)
            vendor.save()
        except Vendor.DoesNotExist:
            entity, _ = Entity.objects.get_or_create(entity_id=msg.get('company_code', ''))
            Vendor.objects.create(
                name=msg.get('short_name', ''),
                vendor_id=msg.get('code', ''),
                entity_id=entity,
                urastic_name=msg.get('name', ''),
                director_name=msg.get('director_name', ''),
                inn_kpp=msg.get('inn', '') + '/' + msg.get('kpp', ''),
                urastic_adress=msg.get('address', ''),
                bank_bik=msg.get('bank_code', ''),
                organization_code=msg.get('organization_code', ''),
                dir_party=msg.get('rec_id', None)
        )


# {
# 	"code": "НЕ-п-000011827",
# 	"company_code": "nel",
# 	"rec_id": "5638268573",
# 	"name": "ООО \"Здороведа\"",
# 	"short_name": "ООО \"Здороведа\"",
# 	"organization_code": "000114625",
# 	"director_name": "Шалашилина М.А.",
# 	"inn": "9718128814",
# 	"kpp": "775101001",
# 	"address": "108808,Россия,г.Москва, Вн.Тер.г.Поселение Первомайское, п. Первомайское, ул. Центральная, д.18, пом.16П",
# 	"bank_code": "044525104"
# }
# class Vendor(models.Model):
#     vendor_id = models.CharField('vendor_id', primary_key=True, max_length=20)  # Field name made lowercase.
#     entity_id = models.ForeignKey(Entity, models.DO_NOTHING, db_column = 'entity_id', db_constraint=False, blank=True, null=True)  # Field name made lowercase.
#     name = models.CharField('Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     urastic_name = models.CharField('UrasticName', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     inn_kpp = models.CharField('INN/KPP', max_length=121, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     director_name = models.CharField('DirectorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     urastic_adress = models.CharField('UrasticAdress', max_length=250, blank=True, null=True)  # Field name made lowercase.
#     account = models.CharField('Account', max_length=35, blank=True, null=True)  # Field name made lowercase.
#     bank_name = models.CharField('BankName', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     bank_bik = models.CharField('BankBik', max_length=15, blank=True, null=True)  # Field name made lowercase.
#     corr_account = models.CharField('CorrAccount', max_length=35, blank=True, null=True)  # Field name made lowercase.
#     dir_party = models.BigIntegerField('DirParty', blank=True, null=True)  # Field name made lowercase.