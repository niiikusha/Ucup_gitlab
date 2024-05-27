# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.forms import ValidationError

class KuCustomer(models.Model):
    payMethod = ( 
        ('Взаимозачет', 'Взаимозачет'),
        ('Оплата', 'Оплата')
    )
    ku_id = models.CharField('ku_id', primary_key=True, editable=False)  # Field name made lowercase.
    customer = models.ForeignKey('Customer', models.DO_NOTHING, db_constraint=False, blank=True, null=True)  # Field name made lowercase. 
    entity = models.ForeignKey('Entity', models.DO_NOTHING, db_constraint=False, blank=True, null=True) 
    period = models.CharField('Period', max_length=10)  # Field name made lowercase.
    date_start = models.DateField('Date_start')  # Field name made lowercase.
    date_end = models.DateField('Date_end', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField('Status', max_length=20)  # Field name made lowercase.
    date_actual = models.DateField('Date_actual', blank=True, null=True)  # Field name made lowercase.
    pay_sum = models.FloatField('pay_sum', blank=True, null=True)  # Field name made lowercase.
    graph_exists = models.BooleanField('graph_Exists', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField('Описание', blank=True, null=True)
    contract = models.CharField('Контракт', blank=True, null=True)
    docu_account = models.CharField('Номер счета в договоре', blank=True, null=True)
    docu_number = models.CharField('Номер договора', blank=True, null=True)
    docu_date = models.DateField('Дата договора', blank=True, null=True)
    docu_subject = models.CharField('Предмет договора', blank=True, null=True)
    pay_method  = models.CharField(choices=payMethod ,  verbose_name='Способ оплаты', blank=True, null=True) 
    subsidiaries = models.BooleanField('Дочерние компании', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'ku_customer'

class KuGraphCustomer(models.Model):
    graph_id = models.AutoField('Graph_id', primary_key=True)  # Используем AutoField для автоматического заполнения  # Field name made lowercase.
    customer = models.ForeignKey('Customer', models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    ku = models.ForeignKey(KuCustomer, models.DO_NOTHING, db_constraint=False, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField('Period', max_length=10, blank=True, null=True)  # Field name made lowercase.
    date_start = models.DateField('Date_start', blank=True, null=True)  # Field name made lowercase.
    date_end = models.DateField('Date_end', blank=True, null=True)  # Field name made lowercase.
    date_calc = models.DateTimeField('Дата расчета', blank=True, null=True)  # Field name made lowercase.
    date_accrual = models.DateField('Дата начисления', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField('Status', max_length=20)  # Field name made lowercase.
    sum_calc = models.FloatField('Sum_calc', blank=True, null=True)  # Field name made lowercase.
    sum_bonus = models.FloatField('Sum_bonus', blank=True, null=True)  # Field name made lowercase.
    percent = models.IntegerField('Percent', blank=True, null=True)  # Field name made lowercase.
    sum_approved = models.FloatField('Sum_approved', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'ku_graph_cuctomer'

class Service(models.Model):
    service_code = models.CharField('Код услуги',  blank=True, null=True ) 
    service_name = models.CharField('Название',  blank=True, null=True)  

    class Meta:
        
        db_table = 'service'

class Article(models.Model):
    article_code = models.CharField('Код статьи',  blank=True, null=True ) 
    article_name = models.CharField('Название',  blank=True, null=True)  

    class Meta:
        
        db_table = 'article'

class PlaceService(models.Model):
    shop_code = models.CharField('Код магазина',  blank=True, null=True ) 
    shop_name = models.CharField('Название',  blank=True, null=True)  
    address = models.CharField('Адрес' ,  blank=True, null=True)  

    class Meta:
        
        db_table = 'place_service'

class PriceList(models.Model):
    date_action = models.DateField('Действует до', blank=True, null=True )
    date_expiration  = models.DateField('истечение срока', blank=True, null=True )
    article_code = models.CharField('Код статьи',  blank=True, null=True ) 
    article_name = models.CharField('Название',  blank=True, null=True)   
    price = models.FloatField('Стоимость',  blank=True, null=True) 
    unit = models.CharField('Единица измерения',  blank=True, null=True ) 

    class Meta:
        
        db_table = 'price_list'

class IncludedService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, db_constraint=False, blank=True, null=True )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, db_constraint=False, blank=True, null=True )
    ratio = models.FloatField('Коэффициент', blank=True, null=True)
    ku = models.ForeignKey(KuCustomer, on_delete=models.CASCADE, db_constraint=False, blank=True, null=True)

    class Meta:
        
        db_table = 'included_service'

class Customer(models.Model):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, db_constraint=False, blank=True, null=True)
    customer_id = models.CharField('vendor_id', primary_key=True , max_length=20)  # Field name made lowercase.
    name = models.CharField('Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    urastic_name = models.CharField('UrasticName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inn_kpp = models.CharField('INN/KPP', max_length=121, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    director_name = models.CharField('DirectorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    urastic_adress = models.CharField('UrasticAdress', max_length=250, blank=True, null=True)  # Field name made lowercase.
    account = models.CharField('Account', max_length=100, blank=True, null=True)  # Field name m2ade lowercase.
    bank_name = models.CharField('BankName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bank_bik = models.CharField('BankBik', max_length=50, blank=True, null=True)  # Field name made lowercase.
    corr_account = models.CharField('CorrAccount', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dir_party = models.CharField('DirParty', blank=True, null=True)  # Field name made lowercase.
    #organization_code = models.CharField('код организации', blank=True, null=True)

    class Meta:
       
        db_table = 'customer'

class ClassifierTest(models.Model):
    classifier_code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=50)
    parent_code = models.CharField(max_length=12)

    class Meta:
        
        db_table = 'app_classifier'

    def __str__(self):
        return f"Код классификатора: {self.classifier_code}, Имя: {self.name}, Код родителя: {self.parent_code}"


class Assortment(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_key = models.CharField('Product_Id', blank=True, null=True)  # Field name made lowercase.
    external_code= models.CharField('', blank=True, null=True)  # Field name made lowercase.
    type_assort = models.CharField('', blank=True, null=True)  # Field name made lowercase.
    store_key = models.BigIntegerField('', blank=True, null=True)
    primaryAccountNum = models.FloatField("primaryAccountNum", blank=True, null=True)
    avg_sales = models.FloatField("avg_sales", blank=True, null=True)
    retail_price = models.FloatField("retail_price", blank=True, null=True)
    multiplicity = models.FloatField("multiplicity", blank=True, null=True)
    class Meta:
       
        db_table = 'assortment'


class Brandclassifier(models.Model):
    classifierid = models.CharField(db_column='ClassifierID', primary_key=True)  # Field name made lowercase.
    brand_name = models.CharField(db_column='Brand_name')  # Field name made lowercase.
    producer_name = models.CharField(db_column='Producer_name')  # Field name made lowercase.

    class Meta:
        
        db_table = 'brand_classifier'


class Classifier(models.Model):
    classifierid = models.CharField('ClassifierID', primary_key=True)  # Field name made lowercase.
    l1 = models.CharField(db_column='L1')  # Field name made lowercase.
    l1_name = models.CharField(db_column='L1_name')  # Field name made lowercase.
    l2 = models.CharField(db_column='L2')  # Field name made lowercase.
    l2_name = models.CharField(db_column='L2_name')  # Field name made lowercase.
    l3 = models.CharField(db_column='L3')  # Field name made lowercase.
    l3_name = models.CharField(db_column='L3_name')  # Field name made lowercase.
    l4 = models.CharField(db_column='L4')  # Field name made lowercase.
    l4_name = models.CharField(db_column='L4_name')  # Field name made lowercase.

    class Meta:
        
        db_table = 'classifier'


# class Customer(models.Model):
#     code = models.CharField('Код', blank=True, null=True)  # Field name made lowercase.
#     entity_id = models.CharField('Код компании', blank=True, null=True)  # Field name made lowercase.
#     name = models.CharField('Название', blank=True, null=True)  # Field name made lowercase.
#     organization_code = models.CharField('Код организации', blank=True, null=True)

#     class Meta:
       
#         db_table = 'customer'

class Category(models.Model):
    hierarchy_key_id = models.BigIntegerField('иерархия', blank=True, null=True)  # Field name made lowercase.
    category_parent = models.BigIntegerField('Род. категория', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField('Наименование')  # Field name made lowercase.
    external_code = models.CharField('Внешний код')  # Field name made lowercase.
    lvl = models.IntegerField('Уровень', blank=True, null=True)  # Field name made lowercase.
    external_id = models.BigIntegerField('Внешний id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'category'

class Entity(models.Model):
    entity_id = models.CharField('entity_id', primary_key=True, max_length=4)  # Field name made lowercase.
    director_name = models.CharField('DirectorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    urastic_name = models.CharField('UrasticName', max_length=100)  # Field name made lowercase.
    name = models.CharField('Name', max_length=100)  # Field name made lowercase.
    urastic_address = models.CharField('UrasticAddress', max_length=250, blank=True, null=True)  # Field name made lowercase.
    inn_kpp = models.CharField('INN\\KPP', max_length=121, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bank_name = models.CharField('BankName', max_length=100)  # Field name made lowercase.
    account = models.CharField('Account', max_length=35)  # Field name made lowercase.
    corr_account = models.CharField('CorrAccount', max_length=35)  # Field name made lowercase.
    bank_bink = models.CharField('BankBink', max_length=15)  # Field name made lowercase.
    merge_id = models.CharField('MergeID', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'entity'

class IncludedProduct(models.Model):
    #ku_id = models.CharField(db_column='KU_id', blank=True, null=True)  # Field name made lowercase.
    ku_id = models.ForeignKey('Ku', on_delete=models.CASCADE, db_column='ku_id', db_constraint=False, blank=True, null=True)  # Field name made lowercase.
    item_type = models.CharField('Item_type', blank=True, null=True)  # Field name made lowercase.
    item_code = models.CharField('Item_code', blank=True, null=True)  # Field name made lowercase.
    item_name = models.CharField('Item_name', blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField('Brand', blank=True, null=True)  # Field name made lowercase.
    producer = models.CharField('Producer', blank=True, null=True)  # Field name made lowercase.
    id = models.BigAutoField('id', primary_key=True) 

    class Meta:
        db_table = 'included_product'


class IncludedProductList(models.Model):
    graph_id = models.BigIntegerField('Graph_id', blank=True, null=True)  # Field name made lowercase.
    product_id = models.ForeignKey('Product', models.DO_NOTHING, db_column='product_id', db_constraint=False, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField('Amount', blank=True, null=True)  # Field name made lowercase.
    invoice_id = models.CharField('Invoice_id', blank=True, null=True)  # Field name made lowercase.
    inc_prod_list = models.BigAutoField(db_column='inc_prod_list', primary_key=True)  # Field name made lowercase.
    rec_id = models.ForeignKey('Venddoclines', models.DO_NOTHING, db_column='rec_id', db_constraint=False, blank=True, null=True)  # Field name made lowercase.
    qty = models.IntegerField('Количество', blank=True, null=True)
    
    class Meta:
        db_table = 'included_product_list'


class Vendor(models.Model):
    vendor_id = models.CharField('vendor_id', primary_key=True, max_length=20)  # Field name made lowercase.
    entity_id = models.ForeignKey(Entity, models.DO_NOTHING, db_column = 'entity_id', db_constraint=False, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField('Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    urastic_name = models.CharField('UrasticName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inn_kpp = models.CharField('INN/KPP', max_length=121, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    director_name = models.CharField('DirectorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    urastic_adress = models.CharField('UrasticAdress', max_length=250, blank=True, null=True)  # Field name made lowercase.
    account = models.CharField('Account', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bank_name = models.CharField('BankName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bank_bik = models.CharField('BankBik', max_length=15, blank=True, null=True)  # Field name made lowercase.
    corr_account = models.CharField('CorrAccount', max_length=35, blank=True, null=True)  # Field name made lowercase.
    dir_party = models.BigIntegerField('DirParty', blank=True, null=True)  # Field name made lowercase.
    organization_code = models.CharField('код организации', blank=True, null=True)

    class Meta:
         
        db_table = 'vendor'

class Ku(models.Model):
    kuType =  ( 
        ('Ретро-бонус', 'Ретро-бонус'),
        ('Услуга', 'Услуга')
    )
    payMethod = ( 
        ('Взаимозачет', 'Взаимозачет'),
        ('Оплата', 'Оплата')
    )
    ku_id = models.CharField('ku_id', primary_key=True, editable=False)  # Field name made lowercase.
    vendor_id = models.ForeignKey(Vendor, models.DO_NOTHING, db_column='vendor_id', db_constraint=False)  # Field name made lowercase. 
    entity_id = models.ForeignKey(Entity, models.DO_NOTHING, db_column='entity_id', db_constraint=False,)  # Field name made lowercase.
    period = models.CharField('Period', max_length=10)  # Field name made lowercase.
    date_start = models.DateField('Date_start')  # Field name made lowercase.
    date_end = models.DateField('Date_end', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField('Status', max_length=20)  # Field name made lowercase.
    date_actual = models.DateField('Date_actual', blank=True, null=True)  # Field name made lowercase.
    base = models.FloatField('Base', blank=True, null=True)  # Field name made lowercase.
    percent = models.IntegerField('Percent', blank=True, null=True)  # Field name made lowercase.
    graph_exists = models.BooleanField('graph_Exists', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField('Описание', blank=True, null=True)
    contract = models.CharField('Контракт', blank=True, null=True)
    product_type = models.CharField('Тип продукта', blank=True, null=True)
    docu_account = models.CharField('Номер счета в договоре', blank=True, null=True)
    docu_name =  models.CharField('Название договора', blank=True, null=True)
    docu_number = models.CharField('Номер договора', blank=True, null=True)
    docu_date = models.DateField('Дата договора', blank=True, null=True)
    docu_subject = models.CharField('Предмет договора', blank=True, null=True)
    tax = models.BooleanField('Налог', blank=True, null=True)
    exclude_return = models.BooleanField('Исключать возвраты', blank=True, null=True)
    negative_turnover =  models.BooleanField('Отрицательный товарооборот', blank=True, null=True)
    ku_type = models.CharField(choices=kuType ,  verbose_name='Тип КУ', blank=True, null=True) 
    pay_method  = models.CharField(choices=payMethod ,  verbose_name='Способ оплаты', blank=True, null=True) 
    subsidiaries = models.BooleanField('Дочерние компании', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'ku'

class BonusCondition(models.Model):
    fix = models.BooleanField(blank=True, null=True)
    criterion = models.FloatField(blank=True, default = 0.0)
    percent_sum = models.FloatField(blank=True, null=True)
    ku_key_id = models.CharField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'bonus_condition'


class KuGraph(models.Model):
    graph_id = models.AutoField('Graph_id', primary_key=True)  # Используем AutoField для автоматического заполнения  # Field name made lowercase.
    vendor_id = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='vendor_id', db_constraint=False,)  # Field name made lowercase.
    ku_id = models.ForeignKey(Ku, on_delete=models.CASCADE, db_column='ku_id', db_constraint=False,)  # Field name made lowercase.
    period = models.CharField('Period', max_length=10)  # Field name made lowercase.
    date_start = models.DateField('Date_start')  # Field name made lowercase.
    date_end = models.DateField('Date_end')  # Field name made lowercase.
    date_calc = models.DateTimeField('Date_calc', blank=True, null=True)  # Field name made lowercase.
    date_accrual = models.DateField('Дата начисления', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField('Status', max_length=20)  # Field name made lowercase.
    sum_calc = models.FloatField('Sum_calc', blank=True, null=True)  # Field name made lowercase.
    sum_bonus = models.FloatField('Sum_bonus', blank=True, null=True)  # Field name made lowercase.
    percent = models.IntegerField('Percent', blank=True, null=True)  # Field name made lowercase.
    sum_approved = models.FloatField('Sum_approved', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'ku_graph'


class Product(models.Model):
    itemid = models.CharField('itemId', primary_key=True)  # Field name made lowercase.
    classifier = models.ForeignKey(Classifier, models.DO_NOTHING, db_column='classifier_id', blank=True, null=True, db_constraint=False)  # Field name made lowercase.
    brand = models.ForeignKey(Brandclassifier, models.DO_NOTHING, db_column='brand_id', blank=True, null=True, db_constraint=False)  # Field name made lowercase.
    name = models.CharField('Name', blank=True, null=True)  # Field name made lowercase.
    external_id = models.BigIntegerField('Внешний id', blank=True, null=True)
    brand_name = models.CharField('Название бренда', blank=True, null=True)  # Field name made lowercase.
    category_id = models.BigIntegerField('ключ категории', blank=True, null=True)
    category_name = models.CharField('Название категории', blank=True, null=True)  # Field name made lowercase.
    group_category_id = models.BigIntegerField('id категории группы', blank=True, null=True)
    sub_group_category_id = models.BigIntegerField('Внешний id', blank=True, null=True)
    price_segment = models.CharField('Property 1', blank=True, null=True)
    
    class Meta:
        
        db_table = 'product'


class Venddoc(models.Model):
    vendor_id = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='vendor_id', db_constraint=False, blank=True, null=True)  # Field name made lowercase.
    entity_id = models.ForeignKey(Entity, models.DO_NOTHING, db_column='entity_id', db_constraint=False, blank=True, null=True)  # Field name made lowercase.
    docid = models.CharField('docid', primary_key=True)  # Field name made lowercase.
    doctype = models.CharField('DocType', blank=True, null=True)  # Field name made lowercase.
    invoice_name = models.CharField('Invoice_name', blank=True, null=True)  # Field name made lowercase.
    invoice_number = models.CharField('Invoice_number', blank=True, null=True)  # Field name made lowercase.
    invoice_date = models.DateField('Invoice_date', blank=True, null=True)  # Field name made lowercase.
    purch_number = models.CharField('Purch_number', blank=True, null=True)  # Field name made lowercase.
    purch_date = models.DateField('Purch_date', blank=True, null=True)  # Field name made lowercase.
    invoice_status = models.CharField('InvoiceStatus', blank=True, null=True)  # Field name made lowercase.
    invoice_id = models.BigIntegerField('Invoice_id', blank=True, null=True)  # Field name made lowercase.
    product_amount = models.FloatField('Products_amount', blank=True, null=True)  # Field name made lowercase.
    purchase_type = models.CharField('purch type', blank=True, null=True)
    fully_factured = models.CharField('fully factured', blank=True, null=True)
    sum_product = models.FloatField('Сумма количества продуктов', blank=True, null=True)

    class Meta:
       
        db_table = 'vend_doc'
 
class ExcludedVenddoc(models.Model):
    ku_id = models.ForeignKey('Ku', on_delete=models.CASCADE, db_column='ku_id', blank=True, null=True, db_constraint=False,)
    docid = models.ForeignKey(Venddoc, on_delete=models.CASCADE, db_column='docid', db_constraint=False, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'excluded_vend_doc'

class ExcludedProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_type = models.CharField('Item_type', blank=True, null=True)  
    item_code = models.CharField('Item_code', blank=True, null=True)  
    item_name = models.CharField('Item_name', blank=True, null=True)  
    brand = models.CharField('Brand', blank=True, null=True)  
    producer = models.CharField('Producer', blank=True, null=True)  
    ku_id = models.ForeignKey('Ku', on_delete=models.CASCADE, db_column='ku_id', blank=True, null=True, db_constraint=False,)

    class Meta:
        db_table = 'excluded_product'

class ExcludedProductList(models.Model):
    graph_id = models.ForeignKey(KuGraph, on_delete=models.CASCADE, db_column='graph_id', db_constraint=False, blank=True, null=True)
    product_id = models.ForeignKey('Product', models.DO_NOTHING, db_column='product_id', db_constraint=False, blank=True, null=True)
    amount = models.FloatField('Amount', blank=True, null=True)  # Field name made lowercase.
    invoice_id = models.CharField('Invoice_id', blank=True, null=True)  # Field name made lowercase.
    rec_id = models.ForeignKey('Venddoclines', models.DO_NOTHING, db_column='rec_id', db_constraint=False, blank=True, null=True)
    qty = models.IntegerField('Количество', blank=True, null=True)

    class Meta:
        db_table = 'excluded_product_list'



class Venddoclines(models.Model):
    recid = models.BigAutoField('RecId', primary_key=True, blank=True, default=2567072)  # Field name made lowercase.
    docid = models.ForeignKey(Venddoc, models.DO_NOTHING, db_column='docid', db_constraint=False, blank=True, null=True)  # Field name made lowercase.
    product_id = models.ForeignKey(Product, models.DO_NOTHING, db_column='product_id', db_constraint=False,)  # Field name made lowercase.
    qty = models.FloatField('QTY', blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField('Amount', blank=True, null=True)  # Field name made lowercase.
    amount_vat = models.FloatField('AmountVAT', blank=True, null=True)  # Field name made lowercase.
    vat = models.FloatField('VAT', blank=True, null=True)  # Field name made lowercase.
    invoice_id = models.BigIntegerField('Invoice_id', blank=True, null=True)  # Field name made lowercase.
    entity_id = models.CharField('entity_id', blank=True, null=True)


    class Meta:
        
        db_table = 'vend_doc_lines'


class Manager(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'manager'

class ManagerKu(models.Model):
    manager = models.ForeignKey(Manager, models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    ku = models.ForeignKey(Ku, models.DO_NOTHING, db_constraint=False, blank=True, null=True)

    class Meta:
        db_table = 'manager_ku'

class ManagerKuCustomer(models.Model):
    manager = models.ForeignKey(Manager, models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    ku = models.ForeignKey(KuCustomer, models.DO_NOTHING, db_constraint=False, blank=True, null=True)

    class Meta:
        db_table = 'manager_ku_customer'

class Official(models.Model):
    id = models.BigAutoField(primary_key=True)
    counterparty_name = models.CharField(blank=True, null=True)
    counterparty_post = models.CharField(blank=True, null=True)
    counterparty_docu = models.CharField(blank=True, null=True)
    entity_name = models.CharField(blank=True, null=True)
    entity_post = models.CharField(blank=True, null=True)
    entity_docu = models.CharField(blank=True, null=True)
    ku_id = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'official'

class OfficialCustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    counterparty_name = models.CharField(blank=True, null=True)
    counterparty_post = models.CharField(blank=True, null=True)
    counterparty_docu = models.CharField(blank=True, null=True)
    entity_name = models.CharField(blank=True, null=True)
    entity_post = models.CharField(blank=True, null=True)
    entity_docu = models.CharField(blank=True, null=True)
    ku_id = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'official_customer'

class IncludedVendor(models.Model):
    vendor = models.ForeignKey(Vendor, models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    retention = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    entity = models.ForeignKey(Entity, models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    type_partner = models.CharField(blank=True, null=True)
    ku = models.ForeignKey(Ku,  models.DO_NOTHING, db_constraint=False, blank=True, null=True)

    class Meta:
        db_table = 'included_vendor'

class IncludedVendorCustomer(models.Model):
    vendor = models.ForeignKey(Vendor, models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    retention = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    entity = models.ForeignKey(Entity, models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    type_partner = models.CharField(blank=True, null=True)
    ku = models.ForeignKey(Ku,  models.DO_NOTHING, db_constraint=False, blank=True, null=True)

    class Meta:
        db_table = 'included_vendor_customer'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

