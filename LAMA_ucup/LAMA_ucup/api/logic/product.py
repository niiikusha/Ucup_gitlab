from typing import Optional
from ...models import Product
from django.db.models import Q
from django.db.models.query import QuerySet


class ProductLogic:
    # @staticmethod
    # def get_list(product_id: Optional[str]) -> QuerySet:
    #     condition = Q()
    #     if product_id is not None:
    #         condition |= Q(id=product_id)

    #     condition.connector = Q.AND
    #     return Vendor.objects.filter(condition)
    
    @staticmethod
    def process_product(msg: dict):
        """
            Обрабатывает продукт из топика "queuing.directory.internalCompanies"
        """
        try:
            code = msg.get('code')
            if code is not None:
                product = Product.objects.get(itemid=msg['code'])
                product.category_id = msg['category_id']
                product.name = msg['name']
                product.external_id = msg['rec_id']
                product.category_name = msg['brand_category']
                product.brand_name = msg['name_brand']
                product.group_category_id = msg['group_category_id']
                product.sub_group_category_id = msg['sub_group_category_id']
                product.save()
            external_code = msg.get('external_code')
            if external_code is not None:
                product = Product.objects.get(itemid=msg['external_code'])
                product.category_id = msg['category_id']
                product.name = msg['name']
                product.external_id = msg['external_id']
                product.category_name = msg['brand_category']
                product.brand_name = msg['name_brand']
                product.group_category_id = msg['group_category_id']
                product.sub_group_category_id = msg['sub_group_category_id']
                product.save()
        except Product.DoesNotExist:
            external_code = msg.get('external_code')
            if external_code is not None:
                Product.objects.create(itemid=msg['external_code'], category_id = msg['category_id'], name=msg['name'], 
                                   external_id = msg['external_id'], category_name = msg['brand_category'], brand_name = msg['name_brand'],
                                   group_category_id = msg['group_category_id'], sub_group_category_id = msg['sub_group_category_id']  )
            code = msg.get('code')
            if code is not None:
                Product.objects.create(itemid=msg['code'], category_id = msg['category_id'], name=msg['name'], 
                                   external_id = msg['rec_id'], category_name = msg['brand_category'], brand_name = msg['name_brand'],
                                   group_category_id = msg['group_category_id'], sub_group_category_id = msg['sub_group_category_id']  )

    
    