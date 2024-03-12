from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import *

class ClassifierTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifierTest
        fields = '__all__'

class IncludedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncludedCondition
        fields = '__all__'

class IncludedProductListSerializer(serializers.ModelSerializer):
    product_qty = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    producer_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = IncludedProduct
        fields = ['graph_key', 'product_key', 'amount', 'invoice_id', 'inc_prod_list', 'product_qty',
                   'product_name' ,'category_name', 'producer_name', 'rec_key', 'brand_name']

    def get_product_qty(self, obj):
        try:
            return obj.rec_key.qty if obj.rec_key else None
        except VendDocLine.DoesNotExist:
            return None
        
    def get_product_name(self, obj):
        try:
            return obj.product_key.name if obj.product_key else None
        except Product.DoesNotExist:
            return None
        
    def get_category_name(self, obj):
        try:
            return obj.product_key.classifier_key.l4_name if obj.product_key and obj.product_key.classifier_key else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except Classifier.DoesNotExist:
            return None
        
    def get_producer_name(self, obj):
        try:
            return obj.product_key.brand_key.producer_name if obj.product_key and obj.product_key.brand_key else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except BrandClassifier.DoesNotExist:
            return None
        
    def get_brand_name(self, obj):
        try:
            return obj.product_key.brand_key.brand_name if obj.product_key and obj.product_key.brand_key else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except BrandClassifier.DoesNotExist:
            return None
        
   

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['external_code', 'director_name', 'urastic_name', 'name', 'urastic_address',
                  'inn_kpp', 'bank_name', 'account', 'corr_account', 'bank_bink', 'merge_id']
       

class KuSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()

    class Meta:
        model = Ku
        fields = ['ku_id', 'vendor_key', 'vendor_name', 'entity_key', 'entity_name', 'period', 
                  'date_start', 'date_end', 'status_ku', 'date_actual', 'percent', 'graph_exists',
                  'description', 'contract', 'product_type', 'docu_account', 'docu_name', 'docu_number',
                  'docu_date', 'docu_subject', 'tax', 'exclude_return', 'negative_turnover', 'ku_type', 'pay_method']
    
    def get_entity_name(self, obj):
        try:
            return obj.entity_key.name if obj.entity_key else None
        except Entity.DoesNotExist:
            return None

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_key.name if obj.vendor_key else None
        except Vendor.DoesNotExist:
            return None
   
class KuGraphSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    entity_id = serializers.SerializerMethodField()
    entity_name = serializers.SerializerMethodField()

    class Meta:
        model = KuGraph
        fields = ['sum_approved', 'ku_key', 'vendor_key', 'vendor_name', 'entity_key', 'entity_name', 
                  'period', 'date_start', 'date_end', 'date_calc', 'status', 'sum_calc', 'sum_bonus', 'percent']
    

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_key.name if obj.vendor_key else None
        except Vendor.DoesNotExist:
            return None
        
    def get_entity_name(self, obj):
        try:
            return obj.vendor_key.entity_key.name if obj.vendor_key else None
        except Entity.DoesNotExist:
            return None
        
    def get_entity_id(self, obj):
        try:
            return obj.vendor_key.entity_key.external_code if obj.vendor_key else None
        except Entity.DoesNotExist:
            return None
        

class UserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = '__all__'
      
class BrandClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandClassifier
        fields = ['brand_name', 'producer_name', 'external_code']

 

class ClassifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classifier
        fields = ['id', 'l1', 'l1_name', 'l2', 'l2_name', 'l3', 'l3_name', 'l4', 'l4_name'] 
    


class ProductSerializer(serializers.ModelSerializer):
    l4 = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    classifier_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['external_code', 'name', 'brand_name', 'classifier_name', 'classifier_key', 'l4', 'brand_key'] # 'classifier', 'brand'

    def get_brand_name(self, obj):
        try:
            return obj.brand_key.brand_name if obj.brand_key else None
        except BrandClassifier.DoesNotExist:
            return None

    def get_classifier_name(self, obj):
        try:
            return obj.classifier_key.l4_name if obj.classifier_key else None
        except Classifier.DoesNotExist:
            return None
        
    def get_l4(self, obj):
        try:
            return obj.classifier_key.l4 if obj.classifier_key else None
        except Classifier.DoesNotExist:
            return None

        
class VendorSerializer(serializers.ModelSerializer):
    # entity_name = serializers.SerializerMethodField()
        
    class Meta:
        model = Vendor
        fields = ['id', 'external_code', 'name', 'urastic_name', 'inn_kpp', 
                'director_name', 'urastic_adress', 'account', 'bank_name', 
                'bank_bik', 'corr_account', 'dir_party', 'entity_key', ]
        
    # def get_entity_name(self, obj):
    #     try:
    #         return obj.entity_key.name if obj.entity_key else None
    #     except Entity.DoesNotExist:
    #         return None
    
    
class VendorNameSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vendor
        fields = ['entity_key', 'id', 'name']

class VendDocSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()

    class Meta:
        model = VendDoc
        fields = ['invoice_id','vendor_key', 'vendor_name', 'entity_key', 'entity_name','doc_id', 'doc_type', 'invoice_name', 'invoice_number',
                  'invoice_date', 'purch_number', 'purch_date', 'invoice_status', 'products_amount']
        
        
    def get_entity_name(self, obj):
        try:
            return obj.entity_key.name if obj.entity_key else None
        except Entity.DoesNotExist:
            return None

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_key.name if obj.vendor_key else None
        except Vendor.DoesNotExist:
            return None

      

class VendDocLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendDocLine
        fields = '__all__'
        
# class ProductsSerializer(serializers.ModelSerializer):
#      class Meta:
#         model = Products
#         fields = '__all__'