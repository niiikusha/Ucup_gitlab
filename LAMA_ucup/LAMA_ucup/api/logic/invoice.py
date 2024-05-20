from typing import Optional
from ...models import Venddoc, Vendor, Entity
from django.db.models import Q
from django.db.models.query import QuerySet
from datetime import datetime

class InvoiceLogic:
    @staticmethod
    def process_invoice(msg: dict):
        """
            Обрабатывает продукт из топика "queuing.directory.internalCompanies"
        """
        try:
            invoice = Venddoc.objects.get(docid=msg['code'])
            vendor, _ = Vendor.objects.get_or_create(vendor_id=msg.get('vendor_code', ''))
            entity, _ = Entity.objects.get_or_create(entity_id=msg.get('company_code', ''))
            invoice.vendor_id = vendor
            invoice.purch_number = msg['purchase_code']
            invoice.entity_id = entity
            invoice.invoice_number = msg['document_code']

            invoice_date_str = msg['document_date'].split()[0]
            if '.' in invoice_date_str:
                invoice.invoice_date = datetime.strptime(invoice_date_str, '%d.%m.%Y').strftime('%Y-%m-%d')
            else:
                invoice.invoice_date = datetime.strptime(invoice_date_str, '%m/%d/%Y').strftime('%Y-%m-%d')

            # invoice_date_str = msg['document_date'].split()[0]
            # invoice.invoice_date = datetime.strptime(invoice_date_str, '%d.%m.%Y').strftime('%Y-%m-%d')
            
            invoice_date_purch_str = msg['due_date'].split()[0]
            if '.' in invoice_date_purch_str:
                invoice.purch_date = datetime.strptime(invoice_date_purch_str, '%d.%m.%Y').strftime('%Y-%m-%d')
            else:
                invoice.purch_date = datetime.strptime(invoice_date_purch_str, '%m/%d/%Y').strftime('%Y-%m-%d')


            # invoice_date_purch_str = msg['due_date'].split()[0]
            # invoice.purch_date = datetime.strptime(invoice_date_purch_str, '%d.%m.%Y').strftime('%Y-%m-%d')

            invoice.purchase_type = msg['purchase_type']
            invoice.fully_factured = msg['fully_factured']
            invoice.save()
        except Venddoc.DoesNotExist:
            invoice_date_str = msg['document_date'].split()[0]
            if '.' in invoice_date_str:
                invoice_date_str = datetime.strptime(invoice_date_str, '%d.%m.%Y').strftime('%Y-%m-%d')
            else:
                invoice_date_str = datetime.strptime(invoice_date_str, '%m/%d/%Y').strftime('%Y-%m-%d')

            invoice_date_purch_str = msg['due_date'].split()[0]
            if '.' in invoice_date_purch_str:
                invoice_date_purch_str = datetime.strptime(invoice_date_purch_str, '%d.%m.%Y').strftime('%Y-%m-%d')
            else:
                invoice_date_purch_str = datetime.strptime(invoice_date_purch_str, '%m/%d/%Y').strftime('%Y-%m-%d')


            entity, _ = Entity.objects.get_or_create(entity_id=msg.get('company_code', ''))
            vendor, _ = Vendor.objects.get_or_create(vendor_id=msg.get('vendor_code', ''))
            Venddoc.objects.create(
                    docid=msg['code'], 
                    vendor_id = vendor, 
                    entity_id = entity,
                    invoice_number = msg['document_code'],
                    purch_number = msg['purchase_code'], 
                    invoice_date = invoice_date_str,
                    purch_date = invoice_date_purch_str, 
                    purchase_type = msg['purchase_type'], 
                    fully_factured = msg['fully_factured']
                )
           
# { VENDOR INVOICE
#  "purchase_code": "АРЗк000358562", +
#  "vendor_code": "АР-п-000000026", +
#  "document_code": "ЕЛнк003785855",
#  "document_date": "29.03.2024 00:00:00", +
#  "due_date": "02.04.2024 00:00:00", +
#  "purchase_type": "Purch", +
#  "code": "АРнзк000288166", + docid
#  "fully_factured": "Yes", +
#  "company_code": "arr" +
# }