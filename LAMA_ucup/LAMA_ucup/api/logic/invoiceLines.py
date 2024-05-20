from typing import Optional
from ...models import Venddoclines, Venddoc, Product
from django.db.models import Q
from django.db.models.query import QuerySet


class InvoiceLinesLogic:
    @staticmethod
    def process_invoice_lines(msg: dict):
        """
            Обрабатывает продукт из топика "queuing.directory.internalCompanies"
        """
        try:
                venddoc_docid, _ = Venddoc.objects.get_or_create(docid=msg.get('invoice_code', ''))
                # entity, _ = Entity.objects.get_or_create(entity_id=msg.get('company_code', ''))
                product_itemid, _ = Product.objects.get_or_create(itemid=msg.get('product_code', ''))

                invoice = Venddoclines.objects.get(docid=venddoc_docid, product_id=product_itemid)

                numbers_dict = {}
                numbers_dict.update({'quantity': msg['quantity'], 'amount': msg['amount'], 'amount_tax': msg['amount_tax'], 'vat_value': msg['vat_value']})
                numbers_result = {'quantity': msg['quantity'], 'amount': msg['amount'], 'amount_tax': msg['amount_tax'], 'vat_value': msg['vat_value']}
                for key, value in numbers_dict.items():
                    value_str = str(value)
                    value_str = value_str.replace(' ', '') #удаляем пробелы
                    ostatok = value_str[-2:] #берем остаток
                    value_cel = value_str[:-3] #берем целое
                    value_cel = value_cel.replace('.', '').replace(',', '') #убираем запятые и точки с целого
                    print(' value_cel ',  value_cel , 'ostatok', ostatok)
                    if key == 'quantity':
                        numbers_result[key]= int(value_cel)
                    else: 
                        numbers_result[key] = value_cel + '.' + ostatok

                invoice.qty = numbers_result['quantity']
                invoice.amount = numbers_result['amount']
                invoice.amount_vat = numbers_result['amount_tax']
                invoice.vat = numbers_result['vat_value']
                # invoice.qty = msg['quantity'].split(',')[0]
                # amount_float = msg['amount'].replace(',', '')
                # amount_float = float(amount_float.replace(' ', ''))
                # invoice.amount = amount_float
                # invoice.amount_vat = msg['amount_tax'].replace(',', '.')
                # invoice.vat = msg['vat_value'].replace(',', '.')

                invoice.entity_id = msg['company_code']
                invoice.save()
        except Venddoclines.DoesNotExist:
            last_recid = Venddoclines.objects.latest('recid').recid
            new_recid = last_recid + 1 
        #    amount_float = msg['amount'].replace(',', '')
        #    amount_float = float(amount_float.replace(' ', ''))
            numbers_dict = {}
            numbers_dict.update({'quantity': msg['quantity'], 'amount': msg['amount'], 'amount_tax': msg['amount_tax'], 'vat_value': msg['vat_value']})
            numbers_result = {'quantity': msg['quantity'], 'amount': msg['amount'], 'amount_tax': msg['amount_tax'], 'vat_value': msg['vat_value']}

            for key, value in numbers_dict.items():
                value_str = str(value)
                value_str = value_str.replace(' ', '') #удаляем пробелы
                ostatok = value_str[-2:] #берем остаток
                value_cel = value_str[:-3] #берем целое
                value_cel = value_cel.replace('.', '').replace(',', '') #убираем запятые и точки с целого
                print(' value_cel ',  value_cel , 'ostatok', ostatok)
                print('str', value_cel + '.' + ostatok)
                if key == 'quantity':
                    numbers_result[key]= int(value_cel)
                else: 
                    numbers_result[key] = value_cel + '.' + ostatok

            venddoc_docid, _ = Venddoc.objects.get_or_create(docid=msg.get('invoice_code', ''))
            product_itemid, _ = Product.objects.get_or_create(itemid=msg.get('product_code', ''))

            Venddoclines.objects.create(recid=new_recid, docid=venddoc_docid, product_id=product_itemid, 
                                    qty = numbers_result['quantity'], amount = numbers_result['amount'], 
                                    amount_vat = numbers_result['amount_tax'], vat = numbers_result['vat_value'],
                                    entity_id = msg['company_code'])
        
           
# { VENDOR INVOICE LINES
#  "product_code": "190682", +
#  "quantity": "30,00", +
#  "amount": "2 011,25", +
#  "amount_tax": "402,25", +
#  "invoice_code": "ГМнзк002161462", +
#  "vat_value": "20,00", +
#  "company_code": "lgm"
# }