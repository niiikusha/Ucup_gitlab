from typing import Optional
from ...models import Category
from django.db.models import Q
from django.db.models.query import QuerySet


class CategoryLogic:
    @staticmethod
    def process_category(msg: dict):
        """
            Обрабатывает продукт из топика "queuing.directory.internalCompanies"
        """
        try:
            external_id = msg.get('external_id')
            if external_id is not None:
                category = Category.objects.get(external_id=msg['external_id'])
                category.hierarchy_key_id = msg['hierarchy_key_id']
                category.category_parent = msg['category_parent']
                category.name = msg['name']
                category.external_code = msg['external_code']
                category.lvl = msg['lvl']
                category.save()
            rec_id = msg.get('rec_id')
            if rec_id is not None:
                category = Category.objects.get(external_id=msg['rec_id'])
                category.hierarchy_key_id = msg['hierarchy_rec_id']
                category.category_parent = msg['parent_rec_id']
                category.name = msg['name']
                category.external_code = msg['code']
                category.lvl = msg['lvl']
                category.save()
        except Category.DoesNotExist:
            external_id = msg.get('external_id')
            if external_id is not None:
                Category.objects.create(external_id=msg['external_id'], hierarchy_key_id=msg['hierarchy_key_id'], 
                                   category_parent = msg['category_parent'], name = msg['name'], external_code = msg['external_code'], lvl = msg['lvl'])
            rec_id = msg.get('rec_id')
            if rec_id is not None:
                Category.objects.create(external_id=msg['rec_id'], hierarchy_key_id=msg['hierarchy_rec_id'], 
                                   category_parent = msg['parent_rec_id'], name = msg['name'], external_code = msg['code'], lvl = msg['lvl'])
           


# { queuing.reference.categories
#  "hierarchy_key_id": "5637144577",
#  "category_parent": "5637377086",
#  "name": "СМЕСИ, СПЕЦИИ, ПРИПРАВЫ, ДОБАВКИ РАСТИТЕЛЬНОГО ПРОИСХОЖДЕНИЯ ВЕС (СП)!",
#  "external_code": "ROOT42000503",
#  "lvl": "5",
#  "external_id": "5637378582"
# }
# {
#  "hierarchy_rec_id": "5637144576",
#  "parent_rec_id": "5637256489",
#  "name": "ДРУГИЕ ПРОДУКТЫ ДЛЯ КОШЕК",
#  "code": "Ax010O0100",
#  "lvl": "5",
#  "rec_id": "5637257035",
#  "hierarchy_code": "Procurement"
# }