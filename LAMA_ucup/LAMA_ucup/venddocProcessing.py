

from django.db.models import Sum, F
from .models import IncludedProduct, Venddoc, IncludedProductList, KuGraph, Product, Classifier, Venddoclines, ExcludedProduct, ExcludedProductList, ExcludedVenddoc, Entity, Vendor


class VenddocProcessing:
    @staticmethod
    def save_venddoclines_to_included_products(venddoclines_rows, graph_id):
        """
        Сохранить данные из venddoclines_rows в IncludedProductList.
        """
        if venddoclines_rows is not None:
            for venddoclines_row in venddoclines_rows:
                    product_id_id = venddoclines_row.get('product_id_id')
                    recid = venddoclines_row.get('recid')
            # Получите экземпляр Product по идентификатору
                    product_instance = Product.objects.get(itemid=product_id_id)
                    rec_id_instance = Venddoclines.objects.get(recid=recid)
            
                    included_product = IncludedProductList(
                        product_id=product_instance,
                        invoice_id = venddoclines_row.get('docid_id'),
                        amount = venddoclines_row.get('amount'),
                        qty = venddoclines_row.get('qty'),
                        graph_id = graph_id,
                        rec_id =  rec_id_instance,
                    )
                    print('invoice_id', venddoclines_row.get('docid'))
                    included_product.save()

    @staticmethod
    def products_amount_sum_in_range(graph_id, tax, exclude_return, negative_turnover):
        """
        Рассчитать сумму Amount в указанном диапазоне дат и для указанных vendor_id, entity_id и graph_id.
        """
        queryset = IncludedProductList.objects.filter(graph_id=graph_id)

        if not negative_turnover:
            queryset = queryset.filter(amount__gt=0)
            
        if exclude_return:
            queryset = queryset.exclude(rec_id__docid__doctype='4')
            
        if tax:
            sum_amount = queryset.annotate(total_amount=F('amount') + F('rec_id__amount_vat')).aggregate(sum_amount=Sum('total_amount'))['sum_amount'] or 0
        else:
            sum_amount = queryset.aggregate(sum_amount=Sum('amount'))['sum_amount'] or 0 #all

        return sum_amount

    @staticmethod
    def products_amount_sum_in_range_vse(start_date, end_date, vendor_id, entity_id, graph_id):
        """
        Найти строки накладных, которые подходят по условиям
        """
        graph_instance = KuGraph.objects.get(graph_id=graph_id)
        #excluded_venddoc = ExcludedVenddoc.objects.filter(ku_id=graph_instance.ku_id)
        included_condition_list = IncludedProduct.objects.filter(ku_id=graph_instance.ku_id)
        excluded_condition_list = ExcludedProduct.objects.filter(ku_id=graph_instance.ku_id)
        included_condition_item_code = IncludedProduct.objects.filter(ku_id=graph_instance.ku_id)
       
        if graph_instance.ku_id.subsidiaries is not None: #если стоит галочка дочерних компаний
            entities_merge = Entity.objects.filter(merge_id=entity_id)
            entity_merge_ids = list(entities_merge.values_list('entity_id', flat=True))
            entity_merge_ids.append(entity_id)
            
            dir_party = graph_instance.ku_id.vendor_id.dir_party
            vendor_dir_party = Vendor.objects.filter(entity_id=entity_merge_ids[0], dir_party = dir_party)
            vendors_dir_party = list(entities_merge.values_list('vendor_id', flat=True))
            vendors_dir_party.append(vendor_id)
            print('vendor_dir_party', vendor_dir_party)
        else:
            entity_merge_ids = entity_id
            vendors_dir_party = vendor_id
        print('entity_merge_ids', entity_merge_ids)
        print('vendors_dir_party', vendors_dir_party)
        print('start_date', start_date)
        print('end_date', end_date)
        excluded_venddoc = ExcludedVenddoc.objects.filter(ku_id = graph_instance.ku_id)

        venddoc_rows = Venddoc.objects.filter( # vendor_id__in=vendors_dir_party,
            vendor_id=vendors_dir_party,
            entity_id=entity_merge_ids,
            invoice_date__gte=start_date,
            invoice_date__lte=end_date
        )
        print('venddoc_rows', venddoc_rows)
        if excluded_venddoc is not None: #исключение накладных
            excluded_docid = excluded_venddoc.values_list('docid', flat=True)
            venddoc_rows = venddoc_rows.exclude(docid__in=excluded_docid)
        
        included_condition_list_all = included_condition_list.filter(item_type="Все")
        included_condition_list_table= included_condition_list.filter(item_type="Таблица")
        included_condition_list_category = included_condition_list.filter(item_type="Категория")
        
        table_item_codes = included_condition_list_table.values_list('item_code', flat=True)

        category_item_codes = included_condition_list_category.values_list('item_code', flat=True) #берем коды в условиях типа Категория
        category_item_codes = list(category_item_codes)
        
        category_classifiers = Classifier.objects.filter(l4__in=category_item_codes) #фильтруем Категории по тем которые даны в условиях
        products_category = Product.objects.filter(classifier__in=category_classifiers) #фильтруем продукты по категориям которые получили выше
        products_itemid_list =  products_category.values_list('itemid', flat=True) #получаем список подходящих продуктов под условия типа Категория

        excluded_condition_list_table= excluded_condition_list.filter(item_type="Таблица")
        excluded_condition_list_category = excluded_condition_list.filter(item_type="Категория")

        excluded_table_item_codes = excluded_condition_list_table.values_list('item_code', flat=True)

        excluded_category_item_codes = excluded_condition_list_category.values_list('item_code', flat=True) #берем коды в условиях типа Категория
        excluded_category_item_codes = list(excluded_category_item_codes)
        
        excluded_category_classifiers = Classifier.objects.filter(l4__in=excluded_category_item_codes) #фильтруем Категории по тем которые даны в условиях
        excluded_products_category = Product.objects.filter(classifier__in=excluded_category_classifiers) #фильтруем продукты по категориям которые получили выше
        excluded_products_itemid_list =  excluded_products_category.values_list('itemid', flat=True) 

        docids = venddoc_rows.values_list('docid', flat=True)

        if included_condition_list_all:
            venddoclines_rows = Venddoclines.objects.filter(docid__in=venddoc_rows.values_list('docid', flat=True)).values()
            

        elif included_condition_list_table and included_condition_list_category:
            venddoclines_rows_table = Venddoclines.objects.filter(docid__in=docids, product_id__in=table_item_codes).values()
            print('venddoclines_rows_table ', venddoclines_rows_table )

            venddoclines_rows_category = Venddoclines.objects.filter(docid__in=docids, product_id__in = products_itemid_list).values()
            print('venddoclines_rows_category ', venddoclines_rows_category )

            venddoclines_rows = venddoclines_rows_table.filter(product_id__in = products_itemid_list)
            print(' venddoclines_rows', venddoclines_rows)
            # return venddoclines_rows

        elif included_condition_list_table:
            venddoclines_rows = Venddoclines.objects.filter(docid__in=docids, product_id__in=table_item_codes).values()

        elif included_condition_list_category:
            venddoclines_rows = Venddoclines.objects.filter(docid__in=docids, product_id__in = products_itemid_list).values()
        #Исключенные товары
        excluded_venddoclines_rows = []

        if excluded_condition_list_table and excluded_condition_list_category:
            excluded_venddoclines_rows_table = Venddoclines.objects.filter(docid__in=docids, product_id__in=excluded_table_item_codes).values()
            print('excluded_venddoclines_rows_table ', excluded_venddoclines_rows_table )

            excluded_venddoclines_rows_category = Venddoclines.objects.filter(docid__in=docids, product_id__in = excluded_products_itemid_list).values()
            print('venddoclines_rows_category ', venddoclines_rows_category )

            excluded_venddoclines_rows = excluded_venddoclines_rows_table.filter(product_id__in = excluded_products_itemid_list)
            print(' excluded_venddoclines_rows', excluded_venddoclines_rows)
            # return excluded_venddoclines_rows

        elif excluded_condition_list_table:
            excluded_venddoclines_rows = Venddoclines.objects.filter(docid__in=docids, product_id__in=excluded_table_item_codes).values()

        elif included_condition_list_category:
            excluded_venddoclines_rows = Venddoclines.objects.filter(docid__in=docids, product_id__in = excluded_products_itemid_list).values()

        if excluded_venddoclines_rows:
            excluded_recids = [row['recid'] for row in excluded_venddoclines_rows]
            venddoclines_rows = venddoclines_rows.exclude(recid__in=excluded_recids)

          
        if excluded_venddoclines_rows is not None: #сохранение исключенных продуктов
            for venddoclines_row in excluded_venddoclines_rows:
                product_id_id = venddoclines_row.get('product_id_id')
                recid = venddoclines_row.get('recid')
                # Получите экземпляр Product по идентификатору
                product_instance = Product.objects.get(itemid=product_id_id)
                rec_id_instance = Venddoclines.objects.get(recid=recid)

                excluded_product = ExcludedProductList(
                    product_id=product_instance,
                    invoice_id=venddoclines_row.get('docid_id'),
                    amount=venddoclines_row.get('amount'),
                    qty = venddoclines_row.get('qty'),
                    graph_id=graph_instance,
                    rec_id=rec_id_instance,
                )
                print('excluded_invoice_id', venddoclines_row.get('docid'))
                excluded_product.save()
            

        # venddoclines_rows = venddoclines_rows.exclude(recid__in=excluded_venddoclines_rows.values('recid'))
        print('venddoclines_rows', venddoclines_rows)
        return venddoclines_rows