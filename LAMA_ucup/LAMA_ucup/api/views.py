import json
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from django.db.models import Q
import calendar
import numpy as np
from django.db.models import F
from ..models import Entity, Ku
from django.db.models import OuterRef, Subquery
from ..graphProcessing import GraphProcessing
from ..kuProcessing import KuProcessing
from ..kuCustomerProcessing import KuCustomerProcessing
from ..graphCustomerProcessing import GraphCustomerProcessing
from ..contractProcessing import ContractProcessing
from ..kafka.consumer import Listener
from django.db.models import Sum
from num2words import num2words


class BasePagination(PageNumberPagination):
    page_size = 50  # Количество записей на странице
    page_size_query_param = 'page_size'
    max_page_size = 1000

#клиенты
class ServiceListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = BasePagination

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ArticleListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = BasePagination

class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class PlaceServiceListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = PlaceService.objects.all()
    serializer_class = PlaceServiceSerializer
    pagination_class = BasePagination

class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = PlaceService.objects.all()
    serializer_class = PlaceServiceSerializer

class PriceListListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PriceListSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = PriceList.objects.all()
        article_code = self.request.query_params.get('article_code', None)

        if article_code:
            queryset = queryset.filter(article_code=article_code)

        return queryset.order_by('-date_action')

class PriceListDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer

class IncludedServiceListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = IncludedServiceSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = IncludedService.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)

        if ku_id:
            queryset = queryset.filter(ku=ku_id)

        return queryset
class IncludedServiceDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = IncludedService.objects.all()
    serializer_class = IncludedServiceSerializer

class CustomerListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomerSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Customer.objects.all().order_by('customer_id')
        entity_ids = self.request.query_params.getlist('entity_id', [])
        customer_id = self.request.query_params.get('customer_id', None)
        
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if entity_ids:
            queryset = queryset.filter(entity__in=entity_ids)
    
        search_query = self.request.query_params.get('search', '') 
        try:
            queryset = queryset.filter( 
                Q(customer_id__icontains=search_query) | 
                Q(name__icontains=search_query) | 
                Q(urastic_name__icontains=search_query) | 
                Q(director_name__icontains=search_query) |
                Q(inn_kpp__icontains=search_query) |
                Q(urastic_adress__icontains=search_query) |
                Q(entity__exact=search_query) 
            )
        except Exception as e:
            print(f"Error in queryset filtering: {e}")

        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset
    
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView): #обновление
    permission_classes = [AllowAny]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class KuGraphCustomerListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = KuGraphCustomerSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = KuGraphCustomer.objects.all().order_by('-graph_id')
        queryset = queryset.annotate(entity_id=F('customer_id__entity_id'))

        ku_ids = self.request.query_params.getlist('ku_id', [])
        entity_ids = self.request.query_params.getlist('entity_id', [])
        customer_ids = self.request.query_params.getlist('customer_id', [])
        periods = self.request.query_params.getlist('period', [])
        statuses = self.request.query_params.getlist('status', [])
        date_start_s = self.request.query_params.get('date_start_s', None)
        date_start_e = self.request.query_params.get('date_start_e', None)
        date_end_s = self.request.query_params.get('date_end_s', None)
        date_end_e = self.request.query_params.get('date_end_e', None)
        date_calc_s= self.request.query_params.get('date_calc_s', None)
        date_calc_e= self.request.query_params.get('date_calc_e', None)
        date_accrual_s= self.request.query_params.get('date_accrual_s', None)
        date_accrual_e= self.request.query_params.get('date_accrual_e', None)
        
        if ku_ids:
            queryset = queryset.filter(ku__in=ku_ids)

        if entity_ids:
            queryset = queryset.filter(customer__entity__in=entity_ids)

        if customer_ids:
            queryset = queryset.filter(customer__in=customer_ids)

        if periods:
            queryset = queryset.filter(period__in=periods)

        if statuses:
            queryset = queryset.filter(status__in=statuses)

        if date_start_s and date_start_e:
            queryset = queryset.filter(date_start__range=[date_start_s, date_start_e])
        
        if date_end_s and date_end_e:
            queryset = queryset.filter(date_end__range=[date_end_s, date_end_e])

        if date_calc_s and date_calc_e:
            queryset = queryset.filter(date_calc__range=[date_calc_s, date_calc_e])

        if date_accrual_s and date_accrual_e:
            queryset = queryset.filter(date_accrual__range=[date_accrual_s, date_accrual_e])
        
        # Добавляем сортировку
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            # Если sortOrder не указан, считаем, что сортировка по возрастанию (ASC)
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset

class KuCustomerListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = KuCustomerSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = KuCustomer.objects.all().order_by('-ku_id')
        ku_ids = self.request.query_params.getlist('ku_id', [])
        entity_ids = self.request.query_params.getlist('entity_id', [])
        customer_ids = self.request.query_params.getlist('customer_id', [])
        period =self.request.query_params.get('period', None)
        statuses = self.request.query_params.getlist('status', [])
        graph_exists = self.request.query_params.getlist('graph_exists', [])
        date_start_s =self.request.query_params.get('date_start_s', None)
        date_start_e =self.request.query_params.get('date_start_e', None)
        date_end_s =self.request.query_params.get('date_end_s', None)
        date_end_e =self.request.query_params.get('date_end_e', None)

        if ku_ids:
            queryset = queryset.filter(ku_id__in=ku_ids)

        if entity_ids:
            queryset = queryset.filter(entity__in=entity_ids)

        if customer_ids:
            queryset = queryset.filter(customer__in=customer_ids)

        if period is not None:
            queryset = queryset.filter(period=period)

        if statuses:
            queryset = queryset.filter(status__in=statuses)

        if graph_exists:
            queryset = queryset.filter(graph_exists__in=graph_exists)

        if date_start_s and date_start_e:
            queryset = queryset.filter(date_start__range=[date_start_s, date_start_e])
        
        if date_end_s and date_end_e:
            queryset = queryset.filter(date_end__range=[date_end_s, date_end_e])

        # Добавляем сортировку
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            # Если sortOrder не указан, считаем, что сортировка по возрастанию (ASC)
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset
    


class KuCustomerDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = KuCustomer.objects.all()
    serializer_class = KuCustomerSerializer
#поставщики
class BonusConditionView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = BonusCondition.objects.all()
    serializer_class = BonusConditionSerializer

class ExcludedVenddocView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = ExcludedVenddoc.objects.all()
    serializer_class = ExcludedVenddocSerializer

class ManagerView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

class OfficialView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = Official.objects.all()
    serializer_class = OfficialSerializer

class OfficialCustomerView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = OfficialCustomer.objects.all()
    serializer_class = OfficialCustomerSerializer

class IncludedVendorView(generics.ListCreateAPIView): #поставщики и договоры
    permission_classes = [AllowAny]
    queryset = IncludedVendor.objects.all()
    serializer_class = IncludedVendorSerializer

class IncludedVendorCustomerView(generics.ListCreateAPIView): #поставщики и договоры
    permission_classes = [AllowAny]
    queryset = IncludedVendorCustomer.objects.all()
    serializer_class = IncludedVendorCustomerSerializer

class ExcludedVenddocFullView(generics.ListAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    serializer_class = VendDocSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = Venddoc.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)

        if ku_id:
            excluded_venddoc = ExcludedVenddoc.objects.filter(ku_id=ku_id)
            docid_list = excluded_venddoc.values_list('docid', flat=True)
            queryset = queryset.filter(docid__in=docid_list)

        return queryset

@api_view(['POST'])
@permission_classes([AllowAny])
def kafka_process(request):
    data = json.loads(request.body)
     # Предполагается, что структура данных совместима с сообщением Kafka
    listener = Listener()
    listener.processor.process_message(data)
    
    return JsonResponse({'message': 'Данные успешно получены и обработаны.'}, status=200)
    
class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Category.objects.all()
        external_id = self.request.query_params.get('external_id', None)

        if external_id:
            queryset = queryset.filter(external_id = external_id)

        return queryset

class BonusConditionList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = BonusCondition.objects.all()
    serializer_class = BonusConditionSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = BonusCondition.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)

        if ku_id:
            queryset = queryset.filter(ku_key_id=ku_id)

        return queryset

class ClassifierTestList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ClassifierTest.objects.all()
    serializer_class = ClassifierTestSerializer

class ExcludedVenddocList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ExcludedVenddoc.objects.all()
    serializer_class = ExcludedVenddocSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = ExcludedVenddoc.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)

        if ku_id:
            queryset = queryset.filter(ku_id=ku_id)

        return queryset

class ManagerListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    pagination_class = BasePagination

class ManagerKuListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ManagerKuSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = ManagerKu.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)

        if ku_id:
            queryset = queryset.filter(ku=ku_id)

        return queryset.order_by('id')
    
class ManagerKuDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = ManagerKu.objects.all()
    serializer_class = ManagerKuSerializer

class ManagerKuCustomerListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ManagerKuCustomerSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = ManagerKuCustomer.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)

        if ku_id:
            queryset = queryset.filter(ku=ku_id)

        return queryset.order_by('id')
    
class ManagerKuCustomerDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = ManagerKuCustomer.objects.all()
    serializer_class = ManagerKuCustomerSerializer

class OfficialListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Official.objects.all()
    serializer_class = OfficialSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Official.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)

        if ku_id:
            queryset = queryset.filter(ku_id=ku_id)

        return queryset

class OfficialCustomerListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = OfficialCustomer.objects.all()
    serializer_class = OfficialCustomerSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = OfficialCustomer.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)

        if ku_id:
            queryset = queryset.filter(ku_id=ku_id)

        return queryset
    
class IncludedProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = IncludedProductListSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = IncludedProductList.objects.all().order_by('graph_id')
        graph_id = self.request.query_params.get('graph_id', None)

        if graph_id:
            queryset = queryset.filter(graph_id=graph_id)

        return queryset.order_by('-graph_id')

class ExcludedProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExcludedProductListSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = ExcludedProductList.objects.all().order_by('graph_id')
        graph_id = self.request.query_params.get('graph_id', None)

        if graph_id:
            queryset = queryset.filter(graph_id=graph_id)

        return queryset.order_by('graph_id')
    
class IncludedInvoiceListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VendDocSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = IncludedProductList.objects.all()
    
        graph_id = self.request.query_params.get('graph_id', None)

        if graph_id:
            queryset = queryset.filter(graph_id=graph_id)
            qty_values = queryset.values_list('qty', flat=True)
            total_qty = sum(qty for qty in qty_values if qty is not None)
            
        queryset_venddoc = Venddoc.objects.all().order_by('vendor_id')

        docid_list = queryset.values_list('invoice_id', flat=True)

        queryset_venddoc = queryset_venddoc.filter(docid__in=docid_list)

        # venddoclines__qty
        # queryset_venddoc = queryset_venddoc.annotate(total_qty=total_qty)

        # Добавление total_qty к каждому объекту Venddoc в queryset
        for venddoc in queryset_venddoc:
            venddoc.total_qty = total_qty
        return queryset_venddoc

class EntityListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EntitySerializer

    def get_queryset(self):
        queryset = Entity.objects.all()
        search_query = self.request.query_params.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(entity_id__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(urastic_name__icontains=search_query) |
                Q(director_name__icontains=search_query) |
                Q(urastic_address__icontains=search_query)
            )

        # Добавляем сортировку
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            # Если sortOrder не указан, считаем, что сортировка по возрастанию (ASC)
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset
    

class BrandClassifierListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    queryset = Brandclassifier.objects.all() #данные которые будут возвращаться
    serializer_class = BrandClassifierSerializer #обрабатывает queryset
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Brandclassifier.objects.all()
        queryset_Classifier = Classifier.objects.all()
        vendor_id = self.request.query_params.get('vendor_id', None)
        producer_name = self.request.query_params.get('producer_name', None)
        l4 = self.request.query_params.get('l4', None)

        if l4  is not None:
            queryset_Classifier = queryset_Classifier.filter(l4=l4)
            classifier_ids = queryset_Classifier.values_list('classifierid', flat=True)

            queryset_Product = Product.objects.all()
            queryset_Product = queryset_Product.filter(classifier__in=classifier_ids)
            products_ids = queryset_Product.values_list('brand', flat=True)
            queryset = queryset.filter(classifierid__in=products_ids)

        if producer_name is not None:
            queryset = queryset.filter(producer_name=producer_name)

        if vendor_id:
            queryset_venddoclines = Venddoclines.objects.filter(docid__vendor_id=vendor_id)
            product_ids = queryset_venddoclines.values_list('product_id', flat=True)

            queryset_products = Product.objects.filter(itemid__in =  product_ids )
            brand_ids = queryset_products.values_list('brand', flat=True)

            queryset = queryset.filter(classifierid__in =  brand_ids )

        return queryset

class ClassifierTreeView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    
    serializer_class = ClassifierSerializer #обрабатывает queryset
    

    def get_queryset(self):
        queryset = Classifier.objects.all() #данные которые будут возвращаться
        vendor_id = self.request.query_params.get('vendor_id', None)
        l4 = self.request.query_params.get('l4', None)
        classifier_id = self.request.query_params.get('classifier_id', None)
        
        if l4:
            queryset = queryset.filter(l4=l4)

        if vendor_id:
            queryset_venddoclines = Venddoclines.objects.filter(docid__vendor_id=vendor_id)
            product_ids = queryset_venddoclines.values_list('product_id', flat=True)

            queryset_products = Product.objects.filter(itemid__in =  product_ids )
            classifier_ids = queryset_products.values_list('classifier', flat=True)

            queryset = queryset.filter(classifierid__in =  classifier_ids )

        if classifier_id:
            queryset = queryset.filter(classifier_id = classifier_id)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Множество для хранения уникальных значений classifier_code и parent_code
        unique_values_set = set()

        # Список для хранения результата
        result_list = []
        current_id = 1

        # Проходим по каждому объекту в queryset
        for obj in queryset:
            # Преобразуем объект в словарь, используя нужные поля
            for i in range(1, 5):
                obj_dict = {
                    "id": current_id,
                    "classifier_id": obj.classifierid,
                    "classifier_code": str(getattr(obj, f"l{i}")),
                    "name": str(getattr(obj, f"l{i}_name")),
                    "parent_code": "0" if i == 1 else str(getattr(obj, f"l{i-1}")),
                }

                # Проверяем, не существует ли уже такой элемент
                key = (obj_dict["classifier_code"], obj_dict["parent_code"])
                if key not in unique_values_set:
                    current_id += 1
                    result_list.append(obj_dict)
                    unique_values_set.add(key)

        return Response(result_list)

class ClassifierListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    
    serializer_class = ClassifierSerializer #обрабатывает queryset
    

    def get_queryset(self):
        queryset = Classifier.objects.all() #данные которые будут возвращаться
        vendor_id = self.request.query_params.get('vendor_id', None)
        l4 = self.request.query_params.get('l4', None)

        if l4:
            queryset = queryset.filter(l4=l4)

        if vendor_id:
            queryset_venddoclines = Venddoclines.objects.filter(docid__vendor_id=vendor_id)
            product_ids = queryset_venddoclines.values_list('product_id', flat=True)

            queryset_products = Product.objects.filter(itemid__in =  product_ids )
            classifier_ids = queryset_products.values_list('classifier', flat=True)

            queryset = queryset.filter(classifierid__in =  classifier_ids )

        return queryset

class VendorNameFilterView(generics.ListAPIView): #фильтрация по юр лицу
    permission_classes = [AllowAny] 
    serializer_class =  VendorNameSerializer #обрабатывает queryset
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Vendor.objects.all()
        entity_id = self.request.query_params.get('entity_id', None)
        vendor_id = self.request.query_params.get('vendor_id', None)
        
        # Проверяем, предоставлен ли entityid в параметрах запроса
        if vendor_id:
            # Фильтруем поставщиков на основе предоставленного entityid
            queryset = queryset.filter(vendor_id=vendor_id)
        # Проверяем, предоставлен ли entityid в параметрах запроса
        if entity_id:
            # Фильтруем поставщиков на основе предоставленного entityid
            queryset = queryset.filter(entity_id=entity_id)
    
        return queryset


class VendDocListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VendDocSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Venddoc.objects.all().order_by('-invoice_date')

        entity_ids = self.request.query_params.getlist('entity_id', [])
        vendor_id = self.request.query_params.get('vendor_id', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            queryset = queryset.filter(invoice_date__range=[start_date, end_date])

        if entity_ids:
            queryset = queryset.filter(entity_id__in=entity_ids)

        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)
    
        search_query = self.request.query_params.get('search', '') 

        if search_query: 
            queryset = queryset.filter( 
                Q(vendor_id__exact=search_query) |
                Q(vendor_id__name__icontains=search_query)
                )
        search_queryNumber = self.request.query_params.get('searchNumber', '') 

        if search_queryNumber: 
            queryset = queryset.filter( 
                Q(invoice_number__icontains=search_queryNumber)
                )
            
        # Добавляем сортировку
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            # Если sortOrder не указан, считаем, что сортировка по возрастанию (ASC)
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset

class VendorListViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    serializer_class = VendorSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = Vendor.objects.all().order_by('vendor_id')
        entity_id = self.request.query_params.get('entity_id', None)
        entity_ids = self.request.query_params.getlist('entity_ids', [])
        vendor_id = self.request.query_params.get('vendor_id', None)
        dir_party = self.request.query_params.get('dir_party', None)

        if entity_id:
            queryset = queryset.filter(entity_id=entity_id)

        if entity_ids:
            queryset = queryset.filter(entity_id__in=entity_ids)

        if vendor_id:
            queryset = queryset.filter(vendor_id = vendor_id)
        
        if dir_party:
            queryset = queryset.filter(dir_party = dir_party)
            
        search_query = self.request.query_params.get('search', '') 
        try:
            queryset = queryset.filter( 
                Q(vendor_id__icontains=search_query) | 
                Q(name__icontains=search_query) | 
                Q(urastic_name__icontains=search_query) | 
                Q(director_name__icontains=search_query) |
                Q(inn_kpp__icontains=search_query) |
                Q(urastic_adress__icontains=search_query) |
                Q(entity_id__exact=search_query) # если нужно только айди фильтровать, exact, т.к. он ключ
            )
        except Exception as e:
            print(f"Error in queryset filtering: {e}")

        # Добавляем сортировку
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            # Если sortOrder не указан, считаем, что сортировка по возрастанию (ASC)
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset
        
    
    def list(self, request, *args, **kwargs):
        # Проверяем наличие параметра fields в запросе
        fields_param = request.query_params.get('fields', None)

        # Если параметр fields указан, создаем новый класс сериализатора с нужными полями
        if fields_param:
            fields = fields_param.split(',')
            MetaClass = type('Meta', (), {'model': Vendor, 'fields': fields})
            serializer_class = type('DynamicVendorSerializer', (VendorSerializer,), {'Meta': MetaClass})
        else:
            # Если параметр fields не указан, используем исходный сериализатор
            serializer_class = self.serializer_class

        # Используем новый сериализатор для текущего запроса
        self.serializer_class = serializer_class

        return super().list(request, *args, **kwargs)

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class EntityDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer

class KuListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny] 
    # queryset = Ku.objects.all() #данные которые будут возвращаться
    serializer_class = KuSerializer #обрабатывает queryset
    pagination_class = BasePagination

    # def perform_create(self, serializer):
    #     # Вызываем функцию generate_ku_id перед сохранением экземпляра
    #     print('SERIALIZER.validated_data', serializer.validated_data)
    #     ku_processing = KuProcessing()
    #     ku_processing.create_ku(serializer.validated_data)
        
    #     serializer.save()

    def get_queryset(self):
        queryset = Ku.objects.all().order_by('-ku_id')
        ku_ids = self.request.query_params.getlist('ku_id', [])
        entity_ids = self.request.query_params.getlist('entity_id', [])
        vendor_ids = self.request.query_params.getlist('vendor_id', [])
        period =self.request.query_params.get('period', None)
        statuses = self.request.query_params.getlist('status', [])
        graph_exists = self.request.query_params.getlist('graph_exists', [])
        date_start_s =self.request.query_params.get('date_start_s', None)
        date_start_e =self.request.query_params.get('date_start_e', None)
        date_end_s =self.request.query_params.get('date_end_s', None)
        date_end_e =self.request.query_params.get('date_end_e', None)

        if ku_ids:
            queryset = queryset.filter(ku_id__in=ku_ids)

        if entity_ids:
            queryset = queryset.filter(entity_id__in=entity_ids)

        if vendor_ids:
            queryset = queryset.filter(vendor_id__in=vendor_ids)

        if period is not None:
            queryset = queryset.filter(period=period)

        if statuses:
            queryset = queryset.filter(status__in=statuses)

        if graph_exists:
            queryset = queryset.filter(graph_exists__in=graph_exists)

        if date_start_s and date_start_e:
            queryset = queryset.filter(date_start__range=[date_start_s, date_start_e])
        
        if date_end_s and date_end_e:
            queryset = queryset.filter(date_end__range=[date_end_s, date_end_e])

        search_query = self.request.query_params.get('search', '') 
        try:
            queryset = queryset.filter( 
                Q(vendor_id__exact=search_query) |
                Q(vendor_id__name__icontains=search_query) 
            )
        except Exception as e:
            print(f"Error in queryset filtering: {e}")

        # Добавляем сортировку
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            # Если sortOrder не указан, считаем, что сортировка по возрастанию (ASC)
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset


@api_view(['POST'])
@permission_classes([AllowAny])
def create_ku_customer(request):
    if request.method == 'POST':
        response_data = {}

        data = JSONParser().parse(request)

        customer = data.get('customer')
        entity = data.get('entity')
        period = data.get('period')
        date_start = data.get('date_start')
        date_end = data.get('date_end', None)
        status_ku = data.get('status', None)
        date_actual = data.get('date_actual', None)
        graph_exists = data.get('graph_exists', None)
        description = data.get('description', None)
        contract = data.get('contract', None)
        pay_sum = data.get('pay_sum', None)
        docu_account = data.get('docu_account', None)
      
        docu_number = data.get('docu_number', None)
        docu_date = data.get('docu_date', None)
        docu_subject = data.get('docu_subject', None)
        
        pay_method = data.get('pay_method')  # Default value if not provided

        try:
            ku_processing = KuCustomerProcessing()
            return ku_processing.create_ku_customer(customer, entity, period, date_start, status_ku, date_end, date_actual, graph_exists,
                                           description, contract, docu_account, docu_number, docu_date, docu_subject, pay_method, pay_sum)
        except Exception as ex:
            response_data['status'] = 'false'
            response_data['message'] = 'Непредвиденная ошибка при создании ку: ' + ex.args[0]
            return JsonResponse(response_data, status=status.HTTP_409_CONFLICT)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def create_ku(request):
    if request.method == 'POST':
        response_data = {}

        data = JSONParser().parse(request)

        vendor_id = data.get('vendor_id')
        entity_id = data.get('entity_id')
        period = data.get('period')
        date_start = data.get('date_start')
        date_end = data.get('date_end', None)
        status_ku = data.get('status', None)
        date_actual = data.get('date_actual', None)
        graph_exists = data.get('graph_exists', None)
        description = data.get('description', None)
        contract = data.get('contract', None)
        product_type = data.get('product_type', None)
        docu_account = data.get('docu_account', None)
        docu_name = data.get('docu_name', None)
        docu_number = data.get('docu_number', None)
        docu_date = data.get('docu_date', None)
        docu_subject = data.get('docu_subject', None)
        tax = data.get('tax', None)
        exclude_return = data.get('exclude_return', None)
        negative_turnover = data.get('negative_turnover', None)
        ku_type = data.get('ku_type' )  # Default value if not provided
        pay_method = data.get('pay_method')  # Default value if not provided

        try:
            ku_processing = KuProcessing()
            return ku_processing.create_ku(vendor_id, entity_id, period, date_start, status_ku, date_end, date_actual, graph_exists,
                                           description, contract, product_type, docu_account, docu_name, docu_number, docu_date, docu_subject,
                                            tax, exclude_return, negative_turnover, ku_type, pay_method)
        except Exception as ex:
            response_data['status'] = 'false'
            response_data['message'] = 'Непредвиденная ошибка при создании ку: ' + ex.args[0]
            return JsonResponse(response_data, status=status.HTTP_409_CONFLICT)
    

class KuAPIUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny] # (IsAuthenticated,)  
    queryset = Ku.objects.all() #данные которые будут возвращаться
    serializer_class = KuSerializer #обрабатывает queryset
    # authentication_classes = (TokenAuthentication, )

class KuDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = Ku.objects.all()
    serializer_class = KuSerializer


class GraphListView(generics.ListCreateAPIView, generics.DestroyAPIView): 
    permission_classes = [AllowAny]
    serializer_class = KuGraphSerializer
    pagination_class = BasePagination
    
    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Проходим по queryset и удаляем каждый объект
        for instance in queryset:
            self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_queryset(self):
        queryset = KuGraph.objects.all().order_by('-graph_id')
        queryset = queryset.annotate(entity_id=F('vendor_id__entity_id'))

        ku_ids = self.request.query_params.getlist('ku_id', [])
        entity_ids = self.request.query_params.getlist('entity_id', [])
        vendor_ids = self.request.query_params.getlist('vendor_id', [])
        periods = self.request.query_params.getlist('period', [])
        statuses = self.request.query_params.getlist('status', [])
        date_start_s = self.request.query_params.get('date_start_s', None)
        date_start_e = self.request.query_params.get('date_start_e', None)
        date_end_s = self.request.query_params.get('date_end_s', None)
        date_end_e = self.request.query_params.get('date_end_e', None)
        date_calc_s= self.request.query_params.get('date_calc_s', None)
        date_calc_e= self.request.query_params.get('date_calc_e', None)
        date_accrual_s= self.request.query_params.get('date_accrual_s', None)
        date_accrual_e= self.request.query_params.get('date_accrual_e', None)
        
        if ku_ids:
            queryset = queryset.filter(ku_id__in=ku_ids)

        if entity_ids:
            queryset = queryset.filter(vendor_id__entity_id__in=entity_ids)

        if vendor_ids:
            queryset = queryset.filter(vendor_id__in=vendor_ids)

        if periods:
            queryset = queryset.filter(period__in=periods)

        if statuses:
            queryset = queryset.filter(status__in=statuses)

        if date_start_s and date_start_e:
            queryset = queryset.filter(date_start__range=[date_start_s, date_start_e])
        
        if date_end_s and date_end_e:
            queryset = queryset.filter(date_end__range=[date_end_s, date_end_e])

        if date_calc_s and date_calc_e:
            queryset = queryset.filter(date_calc__range=[date_calc_s, date_calc_e])

        if date_accrual_s and date_accrual_e:
            queryset = queryset.filter(date_accrual__range=[date_accrual_s, date_accrual_e])
        
        search_query = self.request.query_params.get('search', '') 

        if search_query: 
            queryset = queryset.filter( 
                Q(vendor_id__exact=search_query) |
                Q(vendor_id__name__icontains=search_query)
                )
            
        # Добавляем сортировку
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            # Если sortOrder не указан, считаем, что сортировка по возрастанию (ASC)
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset

class GraphDetailView(generics.RetrieveUpdateDestroyAPIView): #обновление
    permission_classes = [AllowAny]
    queryset = KuGraph.objects.all()
    serializer_class = KuGraphSerializer

class GraphCustomerDetailView(generics.RetrieveUpdateDestroyAPIView): #обновление
    permission_classes = [AllowAny]
    queryset = KuGraphCustomer.objects.all()
    serializer_class = KuGraphCustomerSerializer

class GraphWordslView(generics.RetrieveAPIView): #преобразование расчета в слова
    permission_classes = [AllowAny]
    queryset = KuGraph.objects.all()
    serializer_class = KuGraphSerializer

    def get(self, request, *args, **kwargs):
            instance = self.get_object()
            sum_calc = instance.sum_approved
            # included_product_qty = IncludedProductList.filter(graph_id = instance.graph_id)

            if sum_calc is not None:  # Добавляем проверку на None
                sum_calc_as_words = num2words(sum_calc, lang='ru',  to='currency', currency='RUB')

            else:
                sum_calc_as_words = "None"
            sum_calc_as_words = str(int(sum_calc)) + ' руб. ' + str("{:.0f}".format(sum_calc % 1 * 100)) + ' коп. ' + '(' + sum_calc_as_words + ')'
            # Получение общего количества qty для данного графика
            total_qty = IncludedProductList.objects.filter(graph_id=instance.graph_id).aggregate(total_qty=Sum('qty'))['total_qty']
            total_qty = total_qty if total_qty is not None else 0

            return Response({'sum_calc_words': sum_calc_as_words, 'total_qty': total_qty}, status=status.HTTP_200_OK)
    
class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    queryset = Product.objects.all() #данные которые будут возвращаться
    serializer_class = ProductSerializer #обрабатывает queryset
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Product.objects.all().order_by('itemid')
        vendor_id = self.request.query_params.get('vendor_id', None)
        categories = self.request.query_params.getlist('categories_l4', [])
        itemids = self.request.query_params.get('itemid', None)

        if vendor_id:
            queryset_venddoclines = Venddoclines.objects.filter(docid__vendor_id=vendor_id)
            product_ids = queryset_venddoclines.values_list('product_id', flat=True)
            queryset = queryset.filter(itemid__in =  product_ids )

        if categories:
            queryset = queryset.filter(classifier__l4__in = categories)

        if itemids:
            queryset = queryset.filter(itemid =  itemids )

        search_query = self.request.query_params.get('search', '') 
        try:
            queryset = queryset.filter( 
                Q(itemid__icontains=search_query) | 
                Q(name__icontains=search_query) 
            )
        except Exception as e:
            print(f"Error in queryset filtering: {e}")
        
        # Добавляем сортировку
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            order_by = sort_by
            # Если sortOrder не указан, считаем, что сортировка по возрастанию (ASC)
            sort_order = self.request.query_params.get('sort_order', 'asc')
            if sort_order.lower() == 'desc':
                order_by = F(sort_by).desc()
            queryset = queryset.order_by(order_by)

        return queryset

@api_view(['POST'])
@permission_classes([AllowAny])
def name_contact_create(request):
    try:
        contract_processing = ContractProcessing()
        return contract_processing.create_name_contract(request)
    except Exception as ex:
        response_data = {'error': 'Непредвиденная ошибка при создании наименования контракта: ' + ex.args[0]}
        return JsonResponse(response_data, status=status.HTTP_409_CONFLICT)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def create_graph_new(request):
    try:
        graph_processing = GraphProcessing()
        return graph_processing.create_graph(request)
    except Exception as ex:
        response_data = {'error': 'Непредвиденная ошибка при создании графика: ' + ex.args[0]}
        return JsonResponse(response_data, status=status.HTTP_409_CONFLICT)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_graph_customer(request):
    try:
        graph_processing = GraphCustomerProcessing()
        return graph_processing.create_graph_customer(request)
    except Exception as ex:
        response_data = {'error': 'Непредвиденная ошибка при создании графика: ' + ex.args[0]}
        return JsonResponse(response_data, status=status.HTTP_409_CONFLICT)

@api_view(['POST'])
@permission_classes([AllowAny])
def recalculation_graph(request):
    try:
        graph_processing = GraphProcessing()
        return graph_processing.create_graph(request)
    except Exception as ex:
        response_data = {'error': 'Непредвиденная ошибка при создании графика: ' + ex.args[0]}
        return JsonResponse(response_data, status=status.HTTP_409_CONFLICT)

class ExcludedСonditionListView(generics.ListCreateAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    serializer_class = ExcludedProductSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = ExcludedProduct.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)
        
        if ku_id:
            queryset = queryset.filter(ku_id=ku_id)
    
        return queryset

class ExcludedProductView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = ExcludedProduct.objects.all()
    serializer_class = ExcludedProductSerializer

class IncludedСonditionListView(generics.ListCreateAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    serializer_class = IncludedProductSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = IncludedProduct.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)
        
        # Проверяем, предоставлен ли entityid в параметрах запроса
        if ku_id:
            # Фильтруем поставщиков на основе предоставленного entityid
            queryset = queryset.filter(ku_id=ku_id)
    
        return queryset

class IncludedProductView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = IncludedProduct.objects.all()
    serializer_class = IncludedProductSerializer



class IncludedProductBulkUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = IncludedProduct.objects.all()
    serializer_class = IncludedProductSerializer

    def get_queryset(self):
        queryset = IncludedProduct.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)
        
        # Проверяем, предоставлен ли ku_id в параметрах запроса
        if ku_id:
            # Фильтруем объекты на основе предоставленного ku_id
            queryset = queryset.filter(ku_id=ku_id)

        return queryset

    def update(self, request, *args, **kwargs):
        # Переопределение метода update для обработки обновления нескольких объектов
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)



@api_view(['POST'])
@permission_classes([AllowAny])
def included_products_create(request):
    # Проверяем, являются ли входные данные списком
    if isinstance(request.data, list):
        included_products_data = request.data
    elif isinstance(request.data, dict):
        included_products_data = [request.data]
    else:
        return Response({'error': 'Invalid data format. Expected a list or a dictionary.'}, status=status.HTTP_400_BAD_REQUEST)
    print('included_products_data', included_products_data)
    # Используем many=True при создании сериализатора
    serializer = IncludedProductSerializer(data=included_products_data, many=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def excluded_products_create(request):
    # Проверяем, являются ли входные данные списком
    if isinstance(request.data, list):
        excluded_products_data = request.data
    elif isinstance(request.data, dict):
        excluded_products_data = [request.data]
    else:
        return Response({'error': 'Invalid data format. Expected a list or a dictionary.'}, status=status.HTTP_400_BAD_REQUEST)
    print('Excluded_products_data', excluded_products_data)
    # Используем many=True при создании сериализатора
    serializer = ExcludedProductSerializer(data=excluded_products_data, many=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def products_filter(request): 
    classifier_id = request.query_params.get('classifier_id', None)
    brand_id = request.query_params.get('brand_id', None)
    name = request.query_params.get('name', None)
    # Фильтрация по classifier_id и brand_id, name если они предоставлены в запросе
    queryset = Product.objects.all()
    if classifier_id:
        queryset = queryset.filter(classifier_id=classifier_id)
    if brand_id:
        queryset = queryset.filter(brand_id=brand_id)
    if name:
        queryset = queryset.filter(name=name)

    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(UserSerializer(request.user).data)


@api_view(['POST'])
def user_info(request):
    data = JSONParser().parse(request)
    login = data.get('login', None)
    response_data = {}

    