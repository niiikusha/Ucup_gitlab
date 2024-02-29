import calendar

from LAMA_ucup.api.serializers import KuGraphSerializer
from .models import Ku, KuGraph, Venddoc
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from LAMA_ucup.venddocProcessing import VenddocProcessing

class GraphProcessing:

    @staticmethod
    def create_graph(request):
        input_data = JSONParser().parse(request)
        graph_exists = input_data.get('graph_exists')

        if graph_exists == True:
            return Response({'error': 'Графики уже существуют для этого ku_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        ku_id = input_data.get('ku_id')
        period = input_data.get('period')
        date_start = input_data.get('date_start')
        percent = input_data.get('percent')
        vendor_id = input_data.get('vendor_id')
        entity_id = input_data.get('entity_id')
        date_end_initial = input_data.get('date_end')

        if input_data.get('date_actual'):
            date_end_initial = input_data.get('date_actual')

        year, month, day = map(int, date_start.split('-'))

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

                month = next_month
                year = next_month_year
                day = 1  

        if period == 'Год':
            
            while date_end < date_end_initial:
                
                date_end = f"{year}-{12:02d}-{31:02d}"
                month_start = month
                month_calc = 1
                year_calc = year + 1

                if date_end > date_end_initial: 
                    date_end = date_end_initial

                    month_in_date_end = int(date_end_initial.split("-")[1])
                    month_calc = month_in_date_end % 12 + 1
                    year_calc = year + (1 if month_calc == 1 else 0)
                
                graph_data_list.append({
                    'date_start': f"{year}-{month_start:02d}-{day:02d}",
                    'date_end': date_end,
                    'date_calc': f"{year_calc}-{month_calc:02d}-{date_calc}",
                })

                month = 1
                month_start = 1
                year += 1
                day = 1  

        if period == 'Полгода':

            last_day = calendar.monthrange(year, month)[1] 
            date_end = f"{year}-{month:02d}-{last_day:02d}"
            date_start = f"{year}-{month:02d}-{day:02d}"
            while date_end < date_end_initial:
            
                if month <= 6:
                    date_end = f"{year}-{6:02d}-{30:02d}" 
                    date_calc= f"{year}-{7:02d}-{15:02d}" 
                    month = 7
                else:
                    date_end = f"{year}-{12:02d}-{31:02d}"   
                    date_calc =  f"{year+1}-{1:02d}-{15:02d}" 
                    month = 1

                if date_end > date_end_initial: 
                    date_end = date_end_initial

                graph_data_list.append({
                    'date_start': date_start,
                    'date_end': date_end,
                    'date_calc': date_calc,
                })

                if month <= 6:
                    year += 1
                    date_start = f"{year}-{1:02d}-{1:02d}" 
                else:
                    date_start = f"{year}-{7:02d}-{1:02d}" 

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
            
            if sum_calc:
                date_range['status'] = 'Рассчитано'
            else:
                date_range['status'] = 'Запланировано'

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
            graph_id = serializer_instance.data['graph_id']
            start_date = serializer_instance.data['date_start']
            end_date = serializer_instance.data['date_end']
            
            venddoc_processing = VenddocProcessing
            venddoclines_rows = venddoc_processing.products_amount_sum_in_range_vse(start_date, end_date, vendor_id, entity_id, graph_id)
            venddoc_processing.save_venddoclines_to_included_products(venddoclines_rows, graph_id)

            graph_instance = KuGraph.objects.get(graph_id=graph_id)
            sum_calc = venddoc_processing.products_amount_sum_in_range(graph_id)
            sum_bonus = sum_calc * percent / 100
            graph_instance.sum_calc = sum_calc
            graph_instance.sum_bonus = sum_bonus
            graph_instance.status = 'Рассчитано' if sum_calc else 'Запланировано'
            graph_instance.save()
        
        data = [serializer_instance.data for serializer_instance in serializer_instances]
    
        return JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)