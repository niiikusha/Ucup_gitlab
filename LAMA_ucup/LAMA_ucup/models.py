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
    product_id = models.CharField(db_column='Product_Id', blank=True, null=True)  # Field name made lowercase.
    vendor_id = models.CharField(db_column='Vendor_Id', blank=True, null=True)  # Field name made lowercase.
    entity_id = models.CharField(db_column='Entity_Id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
       
        db_table = 'Assortment'


class Brandclassifier(models.Model):
    classifierid = models.CharField(db_column='ClassifierID', primary_key=True)  # Field name made lowercase.
    brand_name = models.CharField(db_column='Brand_name')  # Field name made lowercase.
    producer_name = models.CharField(db_column='Producer_name')  # Field name made lowercase.

    class Meta:
        
        db_table = 'BrandClassifier'


class Classifier(models.Model):
    classifierid = models.CharField(db_column='ClassifierID', primary_key=True)  # Field name made lowercase.
    l1 = models.CharField(db_column='L1')  # Field name made lowercase.
    l1_name = models.CharField(db_column='L1_name')  # Field name made lowercase.
    l2 = models.CharField(db_column='L2')  # Field name made lowercase.
    l2_name = models.CharField(db_column='L2_name')  # Field name made lowercase.
    l3 = models.CharField(db_column='L3')  # Field name made lowercase.
    l3_name = models.CharField(db_column='L3_name')  # Field name made lowercase.
    l4 = models.CharField(db_column='L4')  # Field name made lowercase.
    l4_name = models.CharField(db_column='L4_name')  # Field name made lowercase.

    class Meta:
        
        db_table = 'Classifier'


class Entities(models.Model):
    entity_id = models.CharField(db_column='Entity_id', primary_key=True, max_length=4)  # Field name made lowercase.
    directorname = models.CharField(db_column='DirectorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    urasticname = models.CharField(db_column='UrasticName', max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    urasticaddress = models.CharField(db_column='UrasticAddress', max_length=250, blank=True, null=True)  # Field name made lowercase.
    inn_kpp = models.CharField(db_column='INN\\KPP', max_length=121, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bankname = models.CharField(db_column='BankName', max_length=100)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=35)  # Field name made lowercase.
    corraccount = models.CharField(db_column='CorrAccount', max_length=35)  # Field name made lowercase.
    bankbink = models.CharField(db_column='BankBink', max_length=15)  # Field name made lowercase.
    mergeid = models.CharField(db_column='MergeID', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Entities'

class IncludedProducts(models.Model):
    ku_id = models.CharField(db_column='KU_id', blank=True, null=True)  # Field name made lowercase.
    item_type = models.CharField(db_column='Item_type', blank=True, null=True)  # Field name made lowercase.
    item_code = models.CharField(db_column='Item_code', blank=True, null=True)  # Field name made lowercase.
    item_name = models.CharField(db_column='Item_name', blank=True, null=True)  # Field name made lowercase.
    in_prod_id = models.BigAutoField(db_column='In_prod_Id', primary_key=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', blank=True, null=True)  # Field name made lowercase.
    producer = models.CharField(db_column='Producer', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Included_products'

# class IncludedProductsList(models.Model):
#     graph_id = models.BigIntegerField(db_column='Graph_id', primary_key=True)  # Field name made lowercase. The composite primary key (Graph_id, Product_id) found, that is not supported. The first column is selected.
#     product_id = models.CharField(db_column='Product_id')  # Field name made lowercase.
#     invoice_id = models.CharField(db_column='Invoice_id', blank=True, null=True)  # Field name made lowercase.
#     amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
        
#         db_table = 'Included_products_list'
#         unique_together = (('graph_id', 'product_id'),)


class IncludedProductsList(models.Model):
    graph_id = models.BigIntegerField(db_column='Graph_id', blank=True, null=True)  # Field name made lowercase.
    product_id = models.ForeignKey('Products', models.DO_NOTHING, db_column='Product_id', blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    invoice_id = models.CharField(db_column='Invoice_id', blank=True, null=True)  # Field name made lowercase.
    inc_prod_list = models.BigAutoField(db_column='Inc_prod_list', primary_key=True)  # Field name made lowercase.
    rec_id = models.ForeignKey('Venddoclines', models.DO_NOTHING, db_column='Rec_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'Included_products_list'

class Invoices(models.Model):
    invoice_id = models.BigIntegerField(db_column='Invoice_id', primary_key=True)  # Field name made lowercase.
    vendor_id = models.CharField(db_column='Vendor_id', max_length=20)  # Field name made lowercase.
    doc_id = models.CharField(db_column='Doc_id', max_length=70)  # Field name made lowercase.
    entity_id = models.CharField(db_column='Entity_id', max_length=4)  # Field name made lowercase.
    invoice_name = models.CharField(db_column='Invoice_name', max_length=100)  # Field name made lowercase.
    invoice_number = models.CharField(db_column='Invoice_number', max_length=100)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    purch_number = models.CharField(db_column='Purch_number', max_length=100)  # Field name made lowercase.
    purch_date = models.DateField(db_column='Purch_date')  # Field name made lowercase.
    doc_type = models.IntegerField(db_column='Doc_type')  # Field name made lowercase.
    invoices_status = models.IntegerField(db_column='Invoices_status')  # Field name made lowercase.
    on_off = models.TextField(db_column='On_off', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    base = models.TextField(db_column='Base', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    exclude_return = models.TextField(db_column='Exclude_return', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ofactured = models.TextField(db_column='Ofactured', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ku_type = models.CharField(db_column='KU_type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pay_type = models.CharField(db_column='Pay_type', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Invoices'

class Vendors(models.Model):
    vendor_id = models.CharField(db_column='Vendor_id', primary_key=True, max_length=20)  # Field name made lowercase.
    entity_id = models.ForeignKey(Entities, models.DO_NOTHING, db_column='Entity_id', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    urasticname = models.CharField(db_column='UrasticName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inn_kpp = models.CharField(db_column='INN/KPP', max_length=121, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    directorname = models.CharField(db_column='DirectorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    urasticadress = models.CharField(db_column='UrasticAdress', max_length=250, blank=True, null=True)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bankname = models.CharField(db_column='BankName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bankbik = models.CharField(db_column='BankBik', max_length=15, blank=True, null=True)  # Field name made lowercase.
    corraccount = models.CharField(db_column='CorrAccount', max_length=35, blank=True, null=True)  # Field name made lowercase.
    dirparty = models.BigIntegerField(db_column='DirParty', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Vendors'

class Ku(models.Model):
    ku_id = models.CharField(db_column='Ku_id', primary_key=True, editable=False)  # Field name made lowercase.
    #ku_id = models.BigAutoField(db_column='KU_id', primary_key=True)  # Field name made lowercase.
    vendor_id = models.ForeignKey('Vendors', models.DO_NOTHING, db_column='Vendor_id')  # Field name made lowercase. 
    entity_id = models.ForeignKey(Entities, models.DO_NOTHING, db_column='Entity_id')  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    date_start = models.DateField(db_column='Date_start')  # Field name made lowercase.
    date_end = models.DateField(db_column='Date_end', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20)  # Field name made lowercase.
    date_actual = models.DateField(db_column='Date_actual', blank=True, null=True)  # Field name made lowercase.
    base = models.FloatField(db_column='Base', blank=True, null=True)  # Field name made lowercase.
    percent = models.IntegerField(db_column='Percent', blank=True, null=True)  # Field name made lowercase.
    graph_exists = models.BooleanField(db_column='graph_Exists', blank=True, null=True)  # Field name made lowercase.
    # ku = models.BigAutoField(db_column='Ku')  # Field name made lowercase.
    # ku_id = models.CharField(db_column='Ku_id', primary_key=True)  # Field name made lowercase.
    _count = 0  # Статическая переменная

    class Meta:
        
        db_table = 'KU'

    def save(self, *args, **kwargs): #создание id КУ
        if not self.ku_id:
            if Ku.objects.order_by('-ku_id').first():
                latest_ku = Ku.objects.order_by('-ku_id').first()
                ku_int = int(latest_ku.ku_id[2:])
                Ku._count = ku_int + 1
            else:
                Ku._count = 1
            self.ku_id = f'KY{Ku._count:05}'
        
        if not self.date_end or self.date_end > self.date_start + relativedelta(years=2): #проверка даты окончания
            self.date_actual = self.date_start + relativedelta(years=2)

        if self.date_end < self.date_start:
            raise ValidationError("Дата окончания не должна быть раньше даты начала")
        
        super().save(*args, **kwargs)


class KuGraph(models.Model):
    graph_id = models.AutoField(db_column='Graph_id', primary_key=True)  # Используем AutoField для автоматического заполнения  # Field name made lowercase.
    vendor_id = models.ForeignKey('Vendors', models.DO_NOTHING, db_column='Vendor_id')  # Field name made lowercase.
    ku_id = models.ForeignKey(Ku, models.DO_NOTHING, db_column='Ku_id')  # Field name made lowercase.
    #ku_id = models.ForeignKey(Ku, models.DO_NOTHING, db_column='Ku_id')  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    date_start = models.DateField(db_column='Date_start')  # Field name made lowercase.
    date_end = models.DateField(db_column='Date_end')  # Field name made lowercase.
    date_calc = models.DateField(db_column='Date_calc')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20)  # Field name made lowercase.
    sum_calc = models.FloatField(db_column='Sum_calc', blank=True, null=True)  # Field name made lowercase.
    sum_bonus = models.FloatField(db_column='Sum_bonus', blank=True, null=True)  # Field name made lowercase.
    percent = models.IntegerField(db_column='Percent', blank=True, null=True)  # Field name made lowercase.
    sum_approved = models.FloatField(db_column='Sum_approved', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'KU_graph'


class Products(models.Model):
    itemid = models.CharField(db_column='itemId', primary_key=True)  # Field name made lowercase.
    classifier = models.ForeignKey(Classifier, models.DO_NOTHING, db_column='Classifier_id', blank=True, null=True)  # Field name made lowercase.
    brand = models.ForeignKey(Brandclassifier, models.DO_NOTHING, db_column='Brand_id', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'Products'


class Venddoc(models.Model):
    vendor = models.ForeignKey('Vendors', models.DO_NOTHING, db_column='Vendor_id')  # Field name made lowercase.
    entity = models.ForeignKey(Entities, models.DO_NOTHING, db_column='Entity_id')  # Field name made lowercase.
    docid = models.CharField(db_column='DocID', primary_key=True)  # Field name made lowercase.
    doctype = models.CharField(db_column='DocType')  # Field name made lowercase.
    invoice_name = models.CharField(db_column='Invoice_name')  # Field name made lowercase.
    invoice_number = models.CharField(db_column='Invoice_number')  # Field name made lowercase.
    invoice_date = models.DateField(db_column='Invoice_date')  # Field name made lowercase.
    purch_number = models.CharField(db_column='Purch_number')  # Field name made lowercase.
    purch_date = models.DateField(db_column='Purch_date')  # Field name made lowercase.
    invoicestatus = models.CharField(db_column='InvoiceStatus', blank=True, null=True)  # Field name made lowercase.
    invoice_id = models.BigIntegerField(db_column='Invoice_id', null=True)  # Field name made lowercase.
    products_amount = models.FloatField(db_column='Products_amount', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
       
        db_table = 'VendDoc'

    def save_venddoclines_to_included_products(self, venddoclines_rows, graph_id):
        """
        Сохранить данные из venddoclines_rows в IncludedProductsList.
        """
        if venddoclines_rows is not None:
            for venddoclines_row in venddoclines_rows:
                    included_product = IncludedProductsList(
                        product_id = venddoclines_row.get('product_id'),
                        invoice_id = venddoclines_row.get('docid'),
                        amount = venddoclines_row.get('amount'),
                        graph_id = graph_id,
                        rec_id =  venddoclines_row.get('rec_id')

                        # product_id=venddoclines_row.product_id,
                        # invoice_id=venddoclines_row.docid,
                        # amount=venddoclines_row.amount,
                        # graph_id=graph_id
                    )
                    included_product.save()
        
                
    def products_amount_sum_in_range(self, start_date, end_date, vendor_id, entity_id):
        """
        Рассчитать сумму products_amount в указанном диапазоне дат и для указанных vendor_id и entity_id.
        """
        return (
            Venddoc.objects
            .filter(
                vendor_id=vendor_id,
                entity_id=entity_id,
                invoice_date__gte=start_date,
                invoice_date__lte=end_date
            )
            .aggregate(sum_products_amount=models.Sum('products_amount'))['sum_products_amount'] or 0
        )
    

    def products_amount_sum_in_range_vse(self, start_date, end_date, vendor_id, entity_id):
        """
        Рассчитать сумму products_amount в указанном диапазоне дат и для указанных vendor_id и entity_id.
        """
        venddoc_rows = Venddoc.objects.filter( # Найти строки в Venddoc, соответствующие условиям
            vendor_id=vendor_id,
            entity_id=entity_id,
            invoice_date__gte=start_date,
            invoice_date__lte=end_date
        )
        # venddoclines_rows = []
        venddoclines_rows = Venddoclines.objects.filter(docid__in=venddoc_rows.values_list('docid', flat=True)).values()
    
        # for venddoc_row in venddoc_rows:
        # # Найти все соответствующие строки в Venddoclines
        #     #venddoclines_rows = Venddoclines.objects.filter(docid=venddoc_row.docid)
        #     venddoclines_rows.extend(Venddoclines.objects.filter(docid=venddoc_row.docid).values())
        print('venddoclines_rows', venddoclines_rows)
        return venddoclines_rows
            #self.save_venddoclines_to_included_products(venddoclines_rows)
    
        # Итерировать по всем найденным строкам в Venddoclines
        #     for venddoclines_row in venddoclines_rows:
        #         # Добавить значение amount к общей базе
        #         total_base += venddoclines_row.amount
        # # Установить значение base равным общей базе
        # self.base = total_base
        # self.save()

class Venddoclines(models.Model):
    recid = models.BigIntegerField(db_column='RecId', primary_key=True)  # Field name made lowercase.
    docid = models.ForeignKey(Venddoc, models.DO_NOTHING, db_column='DocID', blank=True, null=True)  # Field name made lowercase.
    product_id = models.CharField(db_column='Product_id')  # Field name made lowercase.
    qty = models.FloatField(db_column='QTY')  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    amountvat = models.FloatField(db_column='AmountVAT')  # Field name made lowercase.
    vat = models.FloatField(db_column='VAT')  # Field name made lowercase.
    invoice_id = models.BigIntegerField(db_column='Invoice_id', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        
        db_table = 'VendDocLines'





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

