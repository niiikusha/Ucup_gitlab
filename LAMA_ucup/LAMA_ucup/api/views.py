import json
from django.forms import model_to_dict
from django.http import JsonResponse
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
from ..models import Entities, Ku
from django.db.models import OuterRef, Subquery
from ..kuProcessing import KuProcessing



class BasePagination(PageNumberPagination):
    page_size = 50  # Количество записей на странице
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ClassifierTestList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ClassifierTest.objects.all()
    serializer_class = ClassifierTestSerializer

class IncludedProductsListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = IncludedProductsListSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = IncludedProductsList.objects.all().order_by('graph_id')
        graph_id = self.request.query_params.get('graph_id', None)

        if graph_id:
            queryset = queryset.filter(graph_id=graph_id)

        return queryset.order_by('graph_id')


class IncludedInvoiceListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    #serializer_class = IncludedProductsListSerializer
    serializer_class = VendDocSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = IncludedProductsList.objects.all()
    
        graph_id = self.request.query_params.get('graph_id', None)

        if graph_id:
            queryset = queryset.filter(graph_id=graph_id)
            
        queryset_venddoc = Venddoc.objects.all().order_by('vendor_id')

        # Получаем список docid из первого queryset
        docid_list = queryset.values_list('invoice_id', flat=True)

        # Фильтруем второй queryset по docid из первого
        queryset_venddoc = queryset_venddoc.filter(docid__in=docid_list)

        return queryset_venddoc

class EntitiesListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = EntitiesSerializer #обрабатывает queryset
    
    def get_queryset(self):
        queryset = Entities.objects.all()
        search_query = self.request.query_params.get('search', '') 
        if search_query: 
            queryset = queryset.filter( 
                Q(entity_id__icontains=search_query) | 
                Q(name__icontains=search_query) |
                Q(urasticname__icontains=search_query) | 
                Q(directorname__icontains=search_query) | 
                Q(urasticaddress__icontains=search_query) 
            )
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

            queryset_Products = Products.objects.all()
            queryset_Products = queryset_Products.filter(classifier__in=classifier_ids)
            products_ids = queryset_Products.values_list('brand', flat=True)
            queryset = queryset.filter(classifierid__in=products_ids)

        if producer_name is not None:
            queryset = queryset.filter(producer_name=producer_name)

        if vendor_id:
            queryset_venddoclines = Venddoclines.objects.filter(docid__vendor_id=vendor_id)
            product_ids = queryset_venddoclines.values_list('product_id', flat=True)

            queryset_products = Products.objects.filter(itemid__in =  product_ids )
            brand_ids = queryset_products.values_list('brand', flat=True)

            queryset = queryset.filter(classifierid__in =  brand_ids )

        return queryset

class ClassifierTreeView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    
    serializer_class = ClassifierSerializer #обрабатывает queryset
    

    def get_queryset(self):
        queryset = Classifier.objects.all() #данные которые будут возвращаться
        vendor_id = self.request.query_params.get('vendor_id', None)

        if vendor_id:
            queryset_venddoclines = Venddoclines.objects.filter(docid__vendor_id=vendor_id)
            product_ids = queryset_venddoclines.values_list('product_id', flat=True)

            queryset_products = Products.objects.filter(itemid__in =  product_ids )
            classifier_ids = queryset_products.values_list('classifier', flat=True)

            queryset = queryset.filter(classifierid__in =  classifier_ids )

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

        if vendor_id:
            queryset_venddoclines = Venddoclines.objects.filter(docid__vendor_id=vendor_id)
            product_ids = queryset_venddoclines.values_list('product_id', flat=True)

            queryset_products = Products.objects.filter(itemid__in =  product_ids )
            classifier_ids = queryset_products.values_list('classifier', flat=True)

            queryset = queryset.filter(classifierid__in =  classifier_ids )

        return queryset

class VendorsNameFilterView(generics.ListAPIView): #фильтрация по юр лицу
    permission_classes = [AllowAny] 
    serializer_class =  VendorsNameSerializer #обрабатывает queryset
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Vendors.objects.all()
        entity_id = self.request.query_params.get('entity_id', None)
        
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
        queryset = Venddoc.objects.all().order_by('vendor_id')

        #entity_id = self.request.query_params.get('entity_id', None)
        entity_ids = self.request.query_params.getlist('entity_id', [])
        vendor_id = self.request.query_params.get('vendor_id', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            queryset = queryset.filter(invoice_date__range=[start_date, end_date])

        if entity_ids:
            queryset = queryset.filter(entity_id__in=entity_ids).order_by('vendor_id')

        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id).order_by('vendor_id')
    
        search_query = self.request.query_params.get('search', '') 

        if search_query: 
            queryset = queryset.filter( 
                Q(vendor_id__exact=search_query) |
                Q(vendor_id__name__icontains=search_query)
                )

        return queryset

class VendorsListViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    serializer_class = VendorsSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        queryset = Vendors.objects.all().order_by('vendor_id')
        #entity_id = self.request.query_params.get('entity_id', None)
        entity_ids = self.request.query_params.getlist('entity_id', [])
        
        # Проверяем, предоставлен ли entityid в параметрах запроса
        if entity_ids:
            # Фильтруем поставщиков на основе предоставленных entity_ids
            queryset = queryset.filter(entity_id__in=entity_ids)


        search_query = self.request.query_params.get('search', '') 
        try:
            queryset = queryset.filter( 
                Q(vendor_id__icontains=search_query) | 
                Q(name__icontains=search_query) | 
                Q(urasticname__icontains=search_query) | 
                Q(directorname__icontains=search_query) |
                Q(inn_kpp__icontains=search_query) |
                Q(urasticadress__icontains=search_query) |
                Q(entity_id__exact=search_query) | # если нужно только айди фильтровать, exact, т.к. он ключ
                Q(entity_id__name__icontains=search_query)  # и по id, и по name
            )
        except Exception as e:
            print(f"Error in queryset filtering: {e}")
        
        return queryset
        
    
    def list(self, request, *args, **kwargs):
        # Проверяем наличие параметра fields в запросе
        fields_param = request.query_params.get('fields', None)

        # Если параметр fields указан, создаем новый класс сериализатора с нужными полями
        if fields_param:
            fields = fields_param.split(',')
            MetaClass = type('Meta', (), {'model': Vendors, 'fields': fields})
            serializer_class = type('DynamicVendorsSerializer', (VendorsSerializer,), {'Meta': MetaClass})
        else:
            # Если параметр fields не указан, используем исходный сериализатор
            serializer_class = self.serializer_class

        # Используем новый сериализатор для текущего запроса
        self.serializer_class = serializer_class

        return super().list(request, *args, **kwargs)


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
        queryset = Ku.objects.all().order_by('ku_id')
        ku_ids = self.request.query_params.getlist('ku_id', [])
        entity_ids = self.request.query_params.getlist('entity_id', [])
        vendor_id = self.request.query_params.get('vendor_id', None)
        period =self.request.query_params.get('period', None)
        status =self.request.query_params.get('status', None)
        date_start =self.request.query_params.get('date_start', None)
        date_end =self.request.query_params.get('date_end', None)

        if ku_ids:
            queryset = queryset.filter(ku_id__in=ku_ids)

        if entity_ids:
            queryset = queryset.filter(entity_id__in=entity_ids)

        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)

        if period is not None:
            queryset = queryset.filter(period=period)

        if status is not None:
            queryset = queryset.filter(status=status)

        if date_start is not None:
            queryset = queryset.filter(date_start=date_start)

        if date_end is not None:
            queryset = queryset.filter(date_end=date_end)

        search_query = self.request.query_params.get('search', '') 
        try:
            queryset = queryset.filter( 
                Q(vendor_id__exact=search_query) |
                Q(vendor_id__name__icontains=search_query) 
            )
        except Exception as e:
            print(f"Error in queryset filtering: {e}")
        return queryset.order_by('-ku_id')
    
@api_view(['POST'])
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
        percent  = data.get('percent', None)
        graph_exists = data.get('graph_exists', None)

        try:
            ku_processing = KuProcessing()
            return ku_processing.create_ku(vendor_id, entity_id, period, date_start, status_ku, date_end, date_actual, percent, graph_exists)
        except Exception as ex:
            response_data['status'] = 'false'
            response_data['message'] = 'Непредвиденная ошибка при создании пользователя: ' + ex.args[0]
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
        queryset = KuGraph.objects.all().order_by('graph_id')
        vendor_id = self.request.query_params.get('vendor_id', None)
        ku_ids = self.request.query_params.getlist('ku_id', [])
        period =self.request.query_params.get('period', None)
        status =self.request.query_params.get('status', None)
        date_start =self.request.query_params.get('date_start', None)
        date_end =self.request.query_params.get('date_end', None)

        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)

        if ku_ids:
            queryset = queryset.filter(ku_id__in=ku_ids)

        if period is not None:
            queryset = queryset.filter(period=period)

        if status is not None:
            queryset = queryset.filter(status=status)

        if date_start is not None:
            queryset = queryset.filter(date_start=date_start)

        if date_end is not None:
            queryset = queryset.filter(date_end=date_end)
        
        search_query = self.request.query_params.get('search', '') 

        if search_query: 
            queryset = queryset.filter( 
                Q(vendor_id__exact=search_query) |
                Q(vendor_id__name__icontains=search_query)
                )

        return queryset.order_by('-graph_id')

class GraphDetailView(generics.RetrieveUpdateDestroyAPIView): #добавление
    permission_classes = [AllowAny]
    queryset = KuGraph.objects.all()
    serializer_class = KuGraphSerializer

class ProductsListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    queryset = Products.objects.all() #данные которые будут возвращаться
    serializer_class = ProductsSerializer #обрабатывает queryset
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = Products.objects.all().order_by('itemid')
        vendor_id = self.request.query_params.get('vendor_id', None)
        categories = self.request.query_params.getlist('categories_l4', [])

        if vendor_id:
            queryset_venddoclines = Venddoclines.objects.filter(docid__vendor_id=vendor_id)
            product_ids = queryset_venddoclines.values_list('product_id', flat=True)
            queryset = queryset.filter(itemid__in =  product_ids )

        if categories:
            queryset = queryset.filter(classifier__l4__in = categories)

        search_query = self.request.query_params.get('search', '') 
        try:
            queryset = queryset.filter( 
                Q(itemid__icontains=search_query) | 
                Q(name__icontains=search_query) 
            )
        except Exception as e:
            print(f"Error in queryset filtering: {e}")
        
        return queryset


@api_view(['POST'])
@permission_classes([AllowAny])
def create_graph(request):
    input_data = JSONParser().parse(request)
    graph_exists = input_data.get('graph_exists')
    if graph_exists == True:
        return Response({'error': 'График с указанным ku_id уже существует'}, status=status.HTTP_400_BAD_REQUEST)
    # Получите данные от пользователя
    ku_id = input_data.get('ku_id')
    period = input_data.get('period')
    
    date_start = input_data.get('date_start')
    date_end_initial = input_data.get('date_end')
    if input_data.get('date_actual'):
        date_end_initial = input_data.get('date_actual')
    percent = input_data.get('percent')
    vendor_id = input_data.get('vendor_id')
    entity_id = input_data.get('entity_id')
    # Разбейте date_start на год, месяц и день
    year, month, day = map(int, date_start.split('-'))

    # Подготовьте данные для создания графиков
    graph_data_list = []

    sum_bonus = 0
    sum_calc = 0
    date_calc = 15
    date_end = f"{year}-{month:02d}-{day:02d}"

    if period == 'Месяц':
        
        while date_end < date_end_initial:
            
            last_day = calendar.monthrange(year, month)[1] #количество дней месяца

            date_end = f"{year}-{month:02d}-{last_day:02d}"

            if date_end > date_end_initial: #проверка последнего графика 
                date_end = date_end_initial

            next_month = month % 12 + 1
            next_month_year = year + (1 if next_month == 1 else 0) #проверка на переполнение месяцев

            graph_data_list.append({
                'date_start': f"{year}-{month:02d}-{day:02d}",
                'date_end': date_end,
                'date_calc': f"{next_month_year}-{next_month:02d}-{date_calc}",
            })

            # Переходите к следующему месяцу
            month = next_month
            year = next_month_year
            day = 1  # Начинайте с первого дня следующего месяца

    if period == 'Год':
        
        while date_end < date_end_initial:
            
            date_end = f"{year}-{12:02d}-{31:02d}"
            month_start = month
            month_calc = 1
            year_calc = year + 1

            if date_end > date_end_initial: #проверка последнего графика 
                date_end = date_end_initial

                month_in_date_end = int(date_end_initial.split("-")[1])
                month_calc = month_in_date_end % 12 + 1
                year_calc = year + (1 if month_calc == 1 else 0) #проверка на переполнение месяцев
            
            graph_data_list.append({
                'date_start': f"{year}-{month_start:02d}-{day:02d}",
                'date_end': date_end,
                'date_calc': f"{year_calc}-{month_calc:02d}-{date_calc}",
            })

            # Переходите к следующему месяцу
            month = 1
            month_start = 1
            year += 1
            day = 1  # Начинайте с первого дня следующего месяца

    if period == 'Полгода':

        last_day = calendar.monthrange(year, month)[1] #количество дней месяца
        date_end = f"{year}-{month:02d}-{last_day:02d}"
        date_start = f"{year}-{month:02d}-{day:02d}"
        while date_end < date_end_initial:
        
            if month <= 6:
                date_end = f"{year}-{6:02d}-{30:02d}" # до конца июня
                date_calc= f"{year}-{7:02d}-{15:02d}" # до конца июня
                month = 7
            else:
                date_end = f"{year}-{12:02d}-{31:02d}"   #до конца декабря  
                date_calc =  f"{year+1}-{1:02d}-{15:02d}" # до конца июня
                month = 1

            if date_end > date_end_initial: #проверка последнего графика 
                date_end = date_end_initial

            graph_data_list.append({
                'date_start': date_start,
                'date_end': date_end,
                'date_calc': date_calc,
            })

            # Переходите к следующему месяцу
            if month <= 6:
                year += 1
                date_start = f"{year}-{1:02d}-{1:02d}" #с начала января
            else:
                date_start = f"{year}-{7:02d}-{1:02d}" #с начала июля

            
        
    if period == 'Квартал':
        
        while date_end < date_end_initial:
            
            last_month_of_quarter = ((month - 1) // 3 + 1) * 3 #последний месяц квартала
            
            last_day = calendar.monthrange(year, last_month_of_quarter )[1] #количество дней месяца # 1 квартал: январь1, февраль2, март3 2 квартал: 4 5 6, 3 квартал

            date_end = f"{year}-{last_month_of_quarter:02d}-{last_day:02d}"

            if date_end > date_end_initial: #проверка последнего графика 
                date_end = date_end_initial

            next_month = last_month_of_quarter % 12 + 1
            next_month_year = year + (1 if next_month == 1 else 0) #проверка на переполнение месяцев
           
            graph_data_list.append({
                'date_start': f"{year}-{month:02d}-{day:02d}",
                'date_end': date_end,
                'date_calc': f"{next_month_year}-{next_month:02d}-{date_calc}",
            })

            # Переходите к следующему месяцу
            month = next_month
            year = next_month_year
            day = 1  

    for date_range in graph_data_list:
        start_date = date_range['date_start']
        end_date = date_range['date_end']
        # Рассчитать sum_calc, используя метод products_amount_sum_in_range
        #sum_calc = Venddoc().products_amount_sum_in_range(start_date, end_date, vendor_id, entity_id)
        #sum_bonus = sum_calc * percent / 100
        
        if sum_calc:
            date_range['status'] = 'Рассчитано'
        else:
            date_range['status'] = 'Запланировано'

        # date_range['sum_calc'] = sum_calc
        # date_range['sum_bonus'] = sum_bonus

        date_range['percent'] = input_data.get('percent')
        date_range['ku_id'] = input_data.get('ku_id')
        date_range['vendor_id'] = input_data.get('vendor_id')
        date_range['period'] = input_data.get('period')
        date_range['entity_id'] = input_data.get('entity_id')
       
    # Создайте экземпляры сериализаторов и сохраните их
    serializer_instances = []
    for graph_data in graph_data_list:
        
        serializer_instance = KuGraphSerializer(data=graph_data)
        
        if serializer_instance.is_valid():
            serializer_instance.save()
            serializer_instances.append(serializer_instance)
        else:
            return JsonResponse({'error': serializer_instance.errors}, status=status.HTTP_400_BAD_REQUEST)

    if graph_data_list:
        ku_instance = Ku.objects.get(ku_id=ku_id)  #при создании графиков заполнение поля "существование графика" в ку
        ku_instance.graph_exists = True
        ku_instance.save()
    
    for serializer_instance in serializer_instances:
    # Получение ID из словаря данных
        graph_id = serializer_instance.data['graph_id']
        start_date = serializer_instance.data['date_start']
        end_date = serializer_instance.data['date_end']
        
        venddoclines_rows = Venddoc().products_amount_sum_in_range_vse(start_date, end_date, vendor_id, entity_id, graph_id)
        print(venddoclines_rows)
        Venddoc().save_venddoclines_to_included_products(venddoclines_rows, graph_id)
        graph_instance = KuGraph.objects.get(graph_id=graph_id)
        sum_calc = Venddoc().products_amount_sum_in_range(graph_id)
        sum_bonus = sum_calc * percent / 100
        graph_instance.sum_calc = sum_calc
        graph_instance.sum_bonus = sum_bonus
        graph_instance.status = 'Рассчитано' if sum_calc else 'Запланировано'
        graph_instance.save()
       # Обновить данные в созданном экземпляре модели
    #     serializer_instance.sum_calc = sum_calc
    #     serializer_instance.sum_bonus = sum_bonus
    #     serializer_instance.status = 'Рассчитано' if sum_calc else 'Запланировано'

    #     # Сохранить обновленный экземпляр
    #     serializer_instance.save()
    #         # serializer_instances.append(serializer_instance)
    # for data in graph_data_list:
    #     serializer_instance = KuGraphSerializer(data=data)
    #     graph_instance = KuGraph.objects.get(graph_id)
    #     print('serializer_instance ', serializer_instance )
    #     sum_calc = Venddoc().products_amount_sum_in_range(graph_id)
    #     sum_bonus = sum_calc * percent / 100
        
    #     # if sum_calc:
    #     #     data['status'] = 'Рассчитано'
    #     # else:
    #     #     data['status'] = 'Запланировано'

    #     data['sum_calc'] = sum_calc
    #     data['sum_bonus'] = sum_bonus
    #     serializer_instance.save()
    # Верните успешный ответ с данными созданных объектов
    data = [serializer_instance.data for serializer_instance in serializer_instances]
    #ids = [item['id'] for item in data]
    return JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def included_products_create(request):
#     included_products_data = JSONParser().parse(request)
#     serializer = IncludedProductsSerializer(data=included_products_data)
    
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IncludedСonditionListView(generics.ListAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    serializer_class = IncludedProductsSerializer

    def get_queryset(self):
        queryset = IncludedProducts.objects.all()
        ku_id = self.request.query_params.get('ku_id', None)
        
        # Проверяем, предоставлен ли entityid в параметрах запроса
        if ku_id:
            # Фильтруем поставщиков на основе предоставленного entityid
            queryset = queryset.filter(ku_id=ku_id)
    
        return queryset

class IncludedProductsView(generics.RetrieveUpdateDestroyAPIView): #добавление/обновление/удаление в одном
    permission_classes = [AllowAny]
    queryset = IncludedProducts.objects.all()
    serializer_class = IncludedProductsSerializer



class IncludedProductsBulkUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = IncludedProducts.objects.all()
    serializer_class = IncludedProductsSerializer

    def get_queryset(self):
        queryset = IncludedProducts.objects.all()
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
    serializer = IncludedProductsSerializer(data=included_products_data, many=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def ku_create(request):
    ku_data = JSONParser().parse(request)
    serializer = KuSerializer(data=ku_data)
    
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
    queryset = Products.objects.all()
    if classifier_id:
        queryset = queryset.filter(classifier_id=classifier_id)
    if brand_id:
        queryset = queryset.filter(brand_id=brand_id)
    if name:
        queryset = queryset.filter(name=name)

    serializer = ProductsSerializer(queryset, many=True)
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
    # try:
    #     user_processing = UserProcessing()
    #     return login
    # except Exception as ex:
    #     response_data['error'] = 'Непредвиденная ошибка: ' + ex.args[0]
    #     return JsonResponse(response_data, status=status.HTTP_409_CONFLICT)

# class ProductsListView(generics.ListAPIView):
#     permission_classes = [AllowAny] 
#     queryset = Products.objects.all() #данные которые будут возвращаться
#     serializer_class = ProductsSerializer #обрабатывает queryset
    