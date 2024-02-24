from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import *

class ClassifierTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifierTest
        fields = '__all__'

class IncludedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncludedProducts
        fields = '__all__'

class IncludedProductsListSerializer(serializers.ModelSerializer):
    product_qty = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    producer_name = serializers.SerializerMethodField()

    class Meta:
        model = IncludedProductsList
        fields = ['graph_id', 'product_id', 'amount', 'invoice_id', 'inc_prod_list', 'product_qty', 'product_name' ,'category_name', 'producer_name']

    def get_product_qty(self, obj):
        try:
            return obj.rec_id.qty if obj.rec_id else None
        except Entities.DoesNotExist:
            return None
        
    def get_product_name(self, obj):
        try:
            return obj.product_id.name if obj.product_id else None
        except Entities.DoesNotExist:
            return None
        

    def get_category_name(self, obj):
        try:
           return obj.product_id.classifier.l4_name if obj.product_id.classifier else None
        except Entities.DoesNotExist:
            return None
        
    def get_producer_name(self, obj):
        try:
            return obj.product_id.brand.brand_name if obj.product_id.brand else None
        except Entities.DoesNotExist:
            return None

   

class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = ['entity_id', 'directorname', 'urasticname', 'name', 'urasticaddress',
                  'inn_kpp', 'bankname', 'account', 'corraccount', 'bankbink', 'mergeid']
       

class KuSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    # ku_id = serializers.ReadOnlyField(source='formatted_ku_id')
    class Meta:
        model = Ku
        fields = ['ku_id', 'vendor_id', 'vendor_name', 'entity_id', 'entity_name', 'period', 'date_start', 'date_end', 'status', 'date_actual', 'base', 'percent', 'graph_exists']
    
    def get_entity_name(self, obj):
        try:
            return obj.entity_id.name if obj.entity_id else None
        except Entities.DoesNotExist:
            return None

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_id.name if obj.vendor_id else None
        except Vendors.DoesNotExist:
            return None
   
class KuGraphSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    entity_id = serializers.SerializerMethodField()
    entity_name = serializers.SerializerMethodField()

    class Meta:
        model = KuGraph
        fields = ['graph_id', 'ku_id', 'vendor_id', 'vendor_name', 'entity_id', 'entity_name', 'period', 'date_start', 'date_end', 'date_calc', 'status', 'sum_calc', 'sum_bonus', 'percent']
    

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_id.name if obj.vendor_id else None
        except Vendors.DoesNotExist:
            return None
        
    def get_entity_name(self, obj):
        try:
            return obj.vendor_id.entity_id.name if obj.vendor_id else None
        except Vendors.DoesNotExist:
            return None
        
    def get_entity_id(self, obj):
        try:
            return obj.vendor_id.entity_id.entity_id if obj.vendor_id else None
        except Vendors.DoesNotExist:
            return None
        

class UserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = '__all__'
      
class BrandClassifierSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = Brandclassifier
        fields = ['classifierid', 'brand_name', 'producer_name']

 

class ClassifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classifier
        fields = ['classifierid', 'l1', 'l1_name', 'l2', 'l2_name', 'l3', 'l3_name', 'l4', 'l4_name'] 
    


class ProductsSerializer(serializers.ModelSerializer):
    l4 = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    classifier_name = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['itemid', 'name', 'brand_name', 'classifier_name', 'classifier', 'l4'] # 'classifier', 'brand'

    def get_brand_name(self, obj):
        try:
            return obj.brand.brand_name if obj.brand else None
        except Brandclassifier.DoesNotExist:
            return None

    def get_classifier_name(self, obj):
        try:
            return obj.classifier.l4_name if obj.classifier else None
        except Classifier.DoesNotExist:
            return None
        
    def get_l4(self, obj):
        try:
            return obj.classifier.l4 if obj.classifier else None
        except Classifier.DoesNotExist:
            return None

class VendorsSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()
        
    class Meta:
        model = Vendors
        fields = ['vendor_id', 'name', 'urasticname', 'inn_kpp', 
                'directorname', 'urasticadress', 'account', 'bankname', 
                'bankbik', 'corraccount', 'dirparty', 'entity_id', 'entity_name' ]
        
    def get_entity_name(self, obj):
        try:
            return obj.entity_id.name if obj.entity_id else None
        except Entities.DoesNotExist:
            return None
    
    
class VendorsNameSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vendors
        fields = ['entity_id','vendor_id', 'name']

class VendDocSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()

    class Meta:
        model = Venddoc
        fields = ['invoice_id','vendor_id', 'vendor_name', 'entity_id', 'entity_name','docid', 'doctype', 'invoice_name', 'invoice_number',
                  'invoice_date', 'purch_number', 'purch_date', 'invoicestatus', 'products_amount']
        
        
    def get_entity_name(self, obj):
        try:
            return obj.entity_id.name if obj.entity_id else None
        except Entities.DoesNotExist:
            return None

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_id.name if obj.vendor_id else None
        except Vendors.DoesNotExist:
            return None

      

class VendDocLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venddoclines
        fields = '__all__'
        
# class ProductsSerializer(serializers.ModelSerializer):
#      class Meta:
#         model = Products
#         fields = '__all__'