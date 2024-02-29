

from django.db.models import Sum
from .models import IncludedProducts, Venddoc, IncludedProductsList, KuGraph, Products, Classifier, Venddoclines


class VenddocProcessing:
    @staticmethod
    def save_venddoclines_to_included_products(venddoclines_rows, graph_id):
        """
        Сохранить данные из venddoclines_rows в IncludedProductsList.
        """
        if venddoclines_rows is not None:
            for venddoclines_row in venddoclines_rows:
                    product_id_id = venddoclines_row.get('product_id_id')
                    recid = venddoclines_row.get('recid')
            # Получите экземпляр Products по идентификатору
                    product_instance = Products.objects.get(itemid=product_id_id)
                    rec_id_instance = Venddoclines.objects.get(recid=recid)
            
                    included_product = IncludedProductsList(
                        product_id=product_instance,
                        invoice_id = venddoclines_row.get('docid_id'),
                        amount = venddoclines_row.get('amount'),
                        graph_id = graph_id,
                        rec_id =  rec_id_instance,
                    )
                    print('invoice_id', venddoclines_row.get('docid'))
                    included_product.save()

    @staticmethod
    def products_amount_sum_in_range(graph_id):
        """
        Рассчитать сумму Amount в указанном диапазоне дат и для указанных vendor_id, entity_id и graph_id.
        """
        return (
            IncludedProductsList.objects
            .filter(
                graph_id=graph_id,
            )
            .aggregate(sum_amount=Sum('amount'))['sum_amount'] or 0
        )

    @staticmethod
    def products_amount_sum_in_range_vse(start_date, end_date, vendor_id, entity_id, graph_id):
        """
        Найти строки накладных, которые подходят по условиям
        """
        graph_instance = KuGraph.objects.get(graph_id=graph_id)
        included_condition_list = IncludedProducts.objects.filter(ku_id=graph_instance.ku_id)
        included_condition_item_code = IncludedProducts.objects.filter(ku_id=graph_instance.ku_id)
       
        venddoc_rows = Venddoc.objects.filter(
            vendor_id=vendor_id,
            entity_id=entity_id,
            invoice_date__gte=start_date,
            invoice_date__lte=end_date
        )

        included_condition_list_all = included_condition_list.filter(item_type="Все")
        included_condition_list_table= included_condition_list.filter(item_type="Таблица")
        included_condition_list_category = included_condition_list.filter(item_type="Категория")

        
        table_item_codes = included_condition_list_table.values_list('item_code', flat=True)

        category_item_codes = included_condition_list_category.values_list('item_code', flat=True) #берем коды в условиях типа Категория
        category_item_codes = list(category_item_codes)
        
        category_classifiers = Classifier.objects.filter(l4__in=category_item_codes) #фильтруем Категории по тем которые даны в условиях
        products_category = Products.objects.filter(classifier__in=category_classifiers) #фильтруем продукты по категориям которые получили выше
        products_itemid_list =  products_category.values_list('itemid', flat=True) #получаем список подходящих продуктов под условия типа Категория

        docids = venddoc_rows.values_list('docid', flat=True)

        if included_condition_list_all:
            venddoclines_rows = Venddoclines.objects.filter(docid__in=venddoc_rows.values_list('docid', flat=True)).values()
            return venddoclines_rows

        elif included_condition_list_table and included_condition_list_category:
            venddoclines_rows_table = Venddoclines.objects.filter(docid__in=docids, product_id__in=table_item_codes).values()
            print('venddoclines_rows_table ', venddoclines_rows_table )

            venddoclines_rows_category = Venddoclines.objects.filter(docid__in=docids, product_id__in = products_itemid_list).values()
            print('venddoclines_rows_category ', venddoclines_rows_category )
            venddoclines_rows = venddoclines_rows_table.filter(product_id__in = products_itemid_list)
            print(' venddoclines_rows', venddoclines_rows)
            return venddoclines_rows

        elif included_condition_list_table:
            venddoclines_rows = Venddoclines.objects.filter(docid__in=docids, product_id__in=table_item_codes).values()

        elif included_condition_list_category:
            venddoclines_rows = Venddoclines.objects.filter(docid__in=docids, product_id__in = products_itemid_list).values()

        

        print('venddoclines_rows', venddoclines_rows)
        return venddoclines_rows