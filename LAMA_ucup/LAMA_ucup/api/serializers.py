from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import *

#клиенты

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class PlaceServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceService
        fields = '__all__'

class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = '__all__'

class IncludedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncludedService
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class KuGraphCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = KuGraphCustomer
        fields = '__all__'

class KuCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = KuCustomer
        fields = '__all__'
#поставщики
class ClassifierTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifierTest
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'

class ManagerKuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerKu
        fields = '__all__'

class ManagerKuCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerKuCustomer
        fields = '__all__'

class OfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Official
        fields = '__all__'

class OfficialCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialCustomer
        fields = '__all__'

class BonusConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusCondition
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ExcludedVenddocSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedVenddoc
        fields = '__all__'

class IncludedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncludedProduct
        fields = '__all__'

class ExcludedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedProduct
        fields = '__all__'

class IncludedProductListSerializer(serializers.ModelSerializer):
    product_qty = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    producer_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = IncludedProductList
        fields = ['graph_id', 'product_id', 'amount', 'invoice_id', 'inc_prod_list', 'product_qty', 'qty',
                   'product_name' ,'category_name', 'producer_name', 'rec_id', 'brand_name']

    def get_product_qty(self, obj):
        try:
            return obj.rec_id.qty if obj.rec_id else None
        except Venddoclines.DoesNotExist:
            return None
        
    def get_product_name(self, obj):
        try:
            return obj.product_id.name if obj.product_id else None
        except Product.DoesNotExist:
            return None
        
    def get_category_name(self, obj):
        try:
            return obj.product_id.classifier.l4_name if obj.product_id and obj.product_id.classifier else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except Classifier.DoesNotExist:
            return None
        
    def get_producer_name(self, obj):
        try:
            return obj.product_id.brand.producer_name if obj.product_id and obj.product_id.brand else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except Brandclassifier.DoesNotExist:
            return None
        
    def get_brand_name(self, obj):
        try:
            return obj.product_id.brand.brand_name if obj.product_id and obj.product_id.brand else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except Brandclassifier.DoesNotExist:
            return None

class ExcludedProductListSerializer(serializers.ModelSerializer):
    product_qty = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    producer_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = ExcludedProductList
        fields = ['graph_id', 'product_id', 'amount', 'invoice_id', 'id', 'product_qty',
                   'product_name' ,'category_name', 'producer_name', 'rec_id', 'brand_name']

    def get_product_qty(self, obj):
        try:
            return obj.rec_id.qty if obj.rec_id else None
        except Venddoclines.DoesNotExist:
            return None
        
    def get_product_name(self, obj):
        try:
            return obj.product_id.name if obj.product_id else None
        except Product.DoesNotExist:
            return None
        
    def get_category_name(self, obj):
        try:
            return obj.product_id.classifier.l4_name if obj.product_id and obj.product_id.classifier else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except Classifier.DoesNotExist:
            return None
        
    def get_producer_name(self, obj):
        try:
            return obj.product_id.brand.producer_name if obj.product_id and obj.product_id.brand else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except Brandclassifier.DoesNotExist:
            return None
        
    def get_brand_name(self, obj):
        try:
            return obj.product_id.brand.brand_name if obj.product_id and obj.product_id.brand else None
        except AttributeError:
            return None
        except Product.DoesNotExist:
            return None
        except Brandclassifier.DoesNotExist:
            return None


    

   

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['entity_id', 'director_name', 'urastic_name', 'name', 'urastic_address',
                  'inn_kpp', 'bank_name', 'account', 'corr_account', 'bank_bink', 'merge_id']
       

class KuSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    # ku_id = serializers.ReadOnlyField(source='formatted_ku_id')
    class Meta:
        model = Ku
        fields = ['ku_id', 'vendor_id', 'vendor_name', 'entity_id', 'entity_name', 'period', 'date_start', 
                  'date_end', 'status', 'date_actual', 'base', 'percent', 'graph_exists', 'description', 
                  'contract', 'product_type', 'docu_account', 'docu_name', 'docu_number', 'docu_date', 
                  'docu_subject', 'tax', 'exclude_return', 'negative_turnover', 'ku_type', 'pay_method', 'subsidiaries']
                
    
    def get_entity_name(self, obj):
        try:
            return obj.entity_id.name if obj.entity_id else None
        except Entity.DoesNotExist:
            return None

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_id.name if obj.vendor_id else None
        except Vendor.DoesNotExist:
            return None
   
class KuGraphSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    entity_id = serializers.SerializerMethodField()
    entity_name = serializers.SerializerMethodField()

    class Meta:
        model = KuGraph
        fields = ['sum_approved', 'graph_id', 'ku_id', 'vendor_id', 'vendor_name', 'entity_id', 'entity_name', 'period', 'date_start', 
                  'date_end', 'date_calc', 'date_accrual','status', 'sum_calc', 'sum_bonus', 'percent']
    

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_id.name if obj.vendor_id else None
        except Vendor.DoesNotExist:
            return None
        
    def get_entity_name(self, obj):
        try:
            return obj.vendor_id.entity_id.name if obj.vendor_id else None
        except Entity.DoesNotExist:
            return None
        
    def get_entity_id(self, obj):
        try:
            return obj.vendor_id.entity_id.entity_id if obj.vendor_id else None
        except Entity.DoesNotExist:
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
    


class ProductSerializer(serializers.ModelSerializer):
    l4 = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    classifier_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['itemid', 'name', 'brand_name', 'classifier_name', 'classifier', 'l4', ] # 'classifier', 'brand'

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

        
class VendorSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()
        
    class Meta:
        model = Vendor
        fields = ['vendor_id', 'name', 'urastic_name', 'inn_kpp', 
                'director_name', 'urastic_adress', 'account', 'bank_name', 
                'bank_bik', 'corr_account', 'dir_party', 'entity_id', 'entity_name' ]
        
    def get_entity_name(self, obj):
        try:
            return obj.entity_id.name if obj.entity_id else None
        except Entity.DoesNotExist:
            return None
    
    
class VendorNameSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vendor
        fields = ['entity_id','vendor_id', 'name']

class VendDocSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()

    class Meta:
        model = Venddoc
        fields = ['invoice_id','vendor_id', 'vendor_name', 'entity_id', 'entity_name','docid', 'doctype', 'invoice_name', 'invoice_number',
                  'invoice_date', 'purch_number', 'purch_date', 'invoice_status', 'product_amount']
        
        
    def get_entity_name(self, obj):
        try:
            return obj.entity_id.name if obj.entity_id else None
        except Entity.DoesNotExist:
            return None

    def get_vendor_name(self, obj):
        try:
            return obj.vendor_id.name if obj.vendor_id else None
        except Vendor.DoesNotExist:
            return None

      

class VendDocLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venddoclines
        fields = '__all__'
        
# class ProductSerializer(serializers.ModelSerializer):
#      class Meta:
#         model = Product
#         fields = '__all__'