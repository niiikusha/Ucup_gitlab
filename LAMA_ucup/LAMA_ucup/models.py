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


class ClassifierTest(models.Model):
    classifier_code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=50)
    parent_code = models.CharField(max_length=12)

    class Meta:
        
        db_table = 'app_classifier'

    def __str__(self):
        return f"Код классификатора: {self.classifier_code}, Имя: {self.name}, Код родителя: {self.parent_code}"
    
class Article(models.Model):
    name = models.CharField(blank=True, null=True)
    id = models.CharField(primary_key=True)

    class Meta:
        
        db_table = 'Article'


class Assortment(models.Model):
    product_id = models.CharField(db_column='Product_Id', blank=True, null=True)  
    vendor_id = models.CharField(db_column='Vendor_Id', blank=True, null=True)  
    entity_id = models.CharField(db_column='Entity_Id', blank=True, null=True)  

    class Meta:
       
        db_table = 'Assortment'


class BrandClassifier(models.Model):
    external_code = models.CharField('Внешний код')  
    brand_name = models.CharField('Название Бренда')  
    producer_name = models.CharField('Имя производителя')  

    class Meta:
        
        db_table = 'BrandClassifier'

    def __str__(self):
        return self.brand_name


class Classifier(models.Model):
    id = models.CharField('id', primary_key=True)  
    l1 = models.CharField('Код первого уровня')  
    l1_name = models.CharField('Название первого уровня')  
    l2 = models.CharField('Код второго уровня')  
    l2_name = models.CharField('Название первого уровня')  
    l3 = models.CharField('Код третьего уровня')  
    l3_name = models.CharField('Название третьего уровня')  
    l4 = models.CharField('Код четвертого уровня')  
    l4_name = models.CharField('Название четвертого уровня')  

    class Meta:
        
        db_table = 'Classifier'

    def __str__(self):
        return self.l4_name


class Entity(models.Model):
    external_code = models.CharField('Внешний ключ', max_length=4)  
    director_name = models.CharField('Имя директора', max_length=100, blank=True, null=True)  
    urastic_name = models.CharField('Полное название', max_length=100)  
    name = models.CharField('Название организации', max_length=100)  
    urastic_address = models.CharField('Адрес', max_length=250, blank=True, null=True)  
    inn_kpp = models.CharField('ИНН\КПП', max_length=121, blank=True, null=True)   
    bank_name = models.CharField('Название банка', max_length=100)  
    account = models.CharField('Номер счета', max_length=35)  
    corr_account = models.CharField('Кор. Счет', max_length=35)  
    bank_bink = models.CharField('BankBink', max_length=15)  
    merge_id = models.CharField('MergeID', max_length=4, blank=True, null=True)  

    class Meta:
        
        db_table = "Entity"

    def __str__(self):
        return self.entity_id


class IncludedProduct(models.Model):  
    ku_key = models.ForeignKey('Ku', on_delete=models.CASCADE,  db_constraint=False, verbose_name='КУ', blank=True)  #сделать ключи для бренда и продюсера и продукта
    item_type = models.CharField(db_column='Item_type', blank=True, null=True)  
    item_code = models.CharField(db_column='Item_code', blank=True, null=True)  
    item_name = models.CharField(db_column='Item_name', blank=True, null=True)   
    brand = models.CharField(db_column='Brand', blank=True, null=True)  
    producer = models.CharField(db_column='Producer', blank=True, null=True)  

    class Meta:
        db_table = 'Included_product'
    
    def __str__(self):
        return self.item_code


class IncludedProductList(models.Model):
    inc_prod_list = models.BigAutoField(db_column='Inc_prod_list', primary_key=True)
    graph_key = models.ForeignKey('KuGraph',  on_delete=models.CASCADE,  db_constraint=False, verbose_name='Номер графика', blank=True, null=True)  
    product_key = models.ForeignKey('Product', on_delete=models.CASCADE,  db_constraint=False, verbose_name='Код продукта', blank=True, null=True)  
    rec_key = models.ForeignKey('Venddocline', on_delete=models.CASCADE,  db_constraint=False, verbose_name='Номер накладной', blank=True, null = True) 
    amount = models.FloatField('Сумма', blank=True, null=True)  
    invoice_id = models.CharField('Номер накладной', blank=True, null=True)     

    class Meta:

        db_table = 'Included_product_list'
    
    def __str__(self):
        return self.product_key

class Vendor(models.Model):
    external_code = models.CharField('Внешний код поставщика', max_length=20)  
    entity_key = models.ForeignKey(Entity, models.DO_NOTHING, on_delete=models.CASCADE,  db_constraint=False, verbose_name='Номер юр. лица', blank=True, null = True) 
    name = models.CharField('Имя поставщика', max_length=100, blank=True, null=True)  
    urastic_name = models.CharField('Полное имя', max_length=100, blank=True, null=True)  
    inn_kpp = models.CharField('INN/KPP', max_length=121, blank=True, null=True)  
    director_name = models.CharField('Имя директора', max_length=100, blank=True, null=True)  
    urastic_adress = models.CharField('Адрес', max_length=250, blank=True, null=True)  
    account = models.CharField('Счет', max_length=35, blank=True, null=True)  
    bank_name = models.CharField('Название банка', max_length=100, blank=True, null=True)  
    bank_bik = models.CharField('БИК банка', max_length=15, blank=True, null=True)  
    corr_account = models.CharField('Номер счета', max_length=35, blank=True, null=True)  
    dir_party = models.BigIntegerField('DirParty', blank=True, null=True)  

    class Meta:
        
        db_table = 'Vendor'

    def __str__(self):
        return self.external_code

class Ku(models.Model):
    statusKu = ( 
        ('Create', 'Создано')
        ('Valid', 'Действует')
        ('Сancel', 'Отменено')
        ('Сlose', 'Закрыто')
    ) 
    kuType =  ( 
        ('RetroBonus', 'Ретро-бонус'),
        ('Service', 'Услуга')
    )
    payMethod = ( 
        ('Mutual', 'Взаиморасчет'),
        ('Payment', 'Оплата')
    )
    ku_id = models.CharField('Ku_id', primary_key=True, editable=False)  
    vendor_key = models.ForeignKey(Vendor,on_delete=models.CASCADE,  db_constraint=False, verbose_name='Поставщик') 
    entity_key = models.ForeignKey(Entity,on_delete=models.CASCADE,  db_constraint=False, verbose_name='Юр. лицо')
    period = models.CharField('Период', max_length=10)  
    date_start = models.DateField('Дата начала')  
    date_end = models.DateField('Дата окончания', blank=True, null=True)   
    date_actual = models.DateField('Актуальная дата', blank=True, null=True)  
    percent = models.IntegerField('Процент', blank=True, null=True) 
    status_ku = models.CharField(choices=statusKu,  verbose_name='Статус ку', default='Create') 
    graph_exists = models.BooleanField('Существование графика', blank=True, null=True)  
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
    ku_type = models.CharField(choices=kuType ,  verbose_name='Тип КУ', default='RetroBonus') 
    pay_method  = models.CharField(choices=payMethod ,  verbose_name='Способ оплаты', default='Mutual') 
   
    class Meta:
        
        db_table = 'KU'

    def __str__(self):
        return self.ku_id

class KuGraph(models.Model):
    statusGraph = ( 
        ('Planned', 'Запланировано')
        ('Calculated', 'Рассчитано')
        ('Approved', 'Утверждено')
    ) 
    vendor_key = models.ForeignKey(Vendor,on_delete=models.CASCADE,  db_constraint=False, verbose_name='Поставщик')  
    ku_key = models.ForeignKey(Ku,on_delete=models.CASCADE,  db_constraint=False, verbose_name='Коммерческое условие')   
    period = models.CharField('Период', max_length=10)  
    date_start = models.DateField('Дата начала')  
    date_end = models.DateField('Дата окончания')  
    date_calc = models.DateField('Дата расчета')  
    status_graph = models.CharField(choices=statusGraph, verbose_name='Статус графика', default='Planned')   
    sum_calc = models.FloatField('Рассчитанная сумма', blank=True, null=True)  
    sum_bonus = models.FloatField('Сумма бонуса', blank=True, null=True)  
    percent = models.IntegerField('Процент', blank=True, null=True)  
    sum_approved = models.FloatField('Утвержденная сумма', blank=True, null=True)  

    class Meta:
        
        db_table = 'KU_graph'


class Product(models.Model):
    external_code = models.CharField('Внешний код продукта')  
    classifier_key = models.ForeignKey(Classifier, on_delete=models.CASCADE,  db_constraint=False, verbose_name='Категория', blank=True, null=True)  
    brand_key = models.ForeignKey(BrandClassifier, on_delete=models.CASCADE,  db_constraint=False, verbose_name='Бренд', blank=True, null=True)  
    name = models.CharField('Название продукта', blank=True, null=True)  

    class Meta:
        
        db_table = 'Product'


class Venddoc(models.Model):
    vendor_key = models.ForeignKey(Vendor, models.DO_NOTHING, db_constraint=False, verbose_name='Поставщик')  
    entity_key = models.ForeignKey(Entity, models.DO_NOTHING, db_constraint=False, verbose_name='Юр лицо')  
    doc_id = models.CharField('Doc_id', primary_key=True)  
    doc_type = models.CharField('DocType')  
    invoice_name = models.CharField('Invoice_name')  
    invoice_number = models.CharField('Invoice_number')  
    invoice_date = models.DateField('Invoice_date')  
    purch_number = models.CharField('Purch_number')  
    purch_date = models.DateField('Purch_date')  
    invoice_status = models.CharField('InvoiceStatus', blank=True, null=True)  
    invoice_id = models.BigIntegerField('Invoice_id', null=True)  
    products_amount = models.FloatField('Products_amount', blank=True, null=True)  
    
    class Meta:
       
        db_table = 'VendDoc'

    # def save_venddoclines_to_included_products(self, venddoclines_rows, graph_id):
    #     """
    #     Сохранить данные из venddoclines_rows в IncludedProductsList.
    #     """
    #     if venddoclines_rows is not None:
    #         for venddoclines_row in venddoclines_rows:
    #                 product_id_id = venddoclines_row.get('product_id_id')
    #                 recid = venddoclines_row.get('recid')
    #         # Получите экземпляр Products по идентификатору
    #                 product_instance = Products.objects.get(itemid=product_id_id)
    #                 rec_id_instance = Venddoclines.objects.get(recid=recid)
            
    #                 included_product = IncludedProductsList(
    #                     product_id=product_instance,
    #                     invoice_id = venddoclines_row.get('docid_id'),
    #                     amount = venddoclines_row.get('amount'),
    #                     graph_id = graph_id,
    #                     rec_id =  rec_id_instance,
    #                 )
    #                 print('invoice_id', venddoclines_row.get('docid'))
    #                 included_product.save()
    
    # def products_amount_sum_in_range(self, graph_id):
    #     """
    #     Рассчитать сумму Amount в указанном диапазоне дат и для указанных vendor_id, entity_id и graph_id.
    #     """
    #     return (
    #         IncludedProductsList.objects
    #         .filter(
    #             graph_id=graph_id,
    #         )
    #         .aggregate(sum_amount=models.Sum('amount'))['sum_amount'] or 0
    #     )

    # def products_amount_sum_in_range_vse(self, start_date, end_date, vendor_id, entity_id, graph_id):
    #     """
    #     Найти строки накладных, которые подходят по условиям
    #     """
    #     graph_instance = KuGraph.objects.get(graph_id=graph_id)
    #     included_condition_list = IncludedProducts.objects.filter(ku_id=graph_instance.ku_id)
    #     included_condition_item_code = IncludedProducts.objects.filter(ku_id=graph_instance.ku_id)
       
    #     venddoc_rows = Venddoc.objects.filter(
    #         vendor_id=vendor_id,
    #         entity_id=entity_id,
    #         invoice_date__gte=start_date,
    #         invoice_date__lte=end_date
    #     )

    #     included_condition_list_all = included_condition_list.filter(item_type="Все")
    #     included_condition_list_table= included_condition_list.filter(item_type="Таблица")
    #     included_condition_list_category = included_condition_list.filter(item_type="Категория")

        
    #     table_item_codes = included_condition_list_table.values_list('item_code', flat=True)

    #     category_item_codes = included_condition_list_category.values_list('item_code', flat=True) #берем коды в условиях типа Категория
    #     category_item_codes = list(category_item_codes)
        
    #     category_classifiers = Classifier.objects.filter(l4__in=category_item_codes) #фильтруем Категории по тем которые даны в условиях
    #     products_category = Products.objects.filter(classifier__in=category_classifiers) #фильтруем продукты по категориям которые получили выше
    #     products_itemid_list =  products_category.values_list('itemid', flat=True) #получаем список подходящих продуктов под условия типа Категория

    #     docids = venddoc_rows.values_list('docid', flat=True)

    #     if included_condition_list_all:
    #         venddoclines_rows = Venddoclines.objects.filter(docid__in=venddoc_rows.values_list('docid', flat=True)).values()
    #         return venddoclines_rows

    #     elif included_condition_list_table and included_condition_list_category:
    #         venddoclines_rows_table = Venddoclines.objects.filter(docid__in=docids, product_id__in=table_item_codes).values()
    #         print('venddoclines_rows_table ', venddoclines_rows_table )

    #         venddoclines_rows_category = Venddoclines.objects.filter(docid__in=docids, product_id__in = products_itemid_list).values()
    #         print('venddoclines_rows_category ', venddoclines_rows_category )
    #         venddoclines_rows = venddoclines_rows_table.filter(product_id__in = products_itemid_list)
    #         print(' venddoclines_rows', venddoclines_rows)
    #         return venddoclines_rows

    #     elif included_condition_list_table:
    #         venddoclines_rows = Venddoclines.objects.filter(docid__in=docids, product_id__in=table_item_codes).values()

    #     elif included_condition_list_category:
    #         venddoclines_rows = Venddoclines.objects.filter(docid__in=docids, product_id__in = products_itemid_list).values()

        

    #     print('venddoclines_rows', venddoclines_rows)
    #     return venddoclines_rows
    
           

class Venddocline(models.Model):
    rec_id = models.BigIntegerField(db_column='RecId', primary_key=True)  
    doc_key = models.ForeignKey(Venddoc, models.DO_NOTHING, db_constraint=False, verbose_name='Накладная', blank=True, null=True)  
    product_key = models.ForeignKey(Product, models.DO_NOTHING,  db_constraint=False, verbose_name='Продукт')  
    qty = models.FloatField('QTY')  
    amount = models.FloatField('Amount')  
    amount_vat = models.FloatField('AmountVAT')  
    vat = models.FloatField('VAT')  
    invoice_id = models.BigIntegerField('Invoice_id', blank=True, null=True)  


    class Meta:
        
        db_table = 'VendDocLine'





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

