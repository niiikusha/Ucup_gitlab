import calendar
from django.utils import timezone
from LAMA_ucup.api.serializers import KuGraphSerializer
from .models import KuCustomer, KuGraphCustomer, Venddoc, BonusCondition
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from LAMA_ucup.venddocProcessing import VenddocProcessing
from LAMA_ucup.graphProcessing import GraphProcessing
from django.db import transaction


class GraphCustomerProcessing:

    @staticmethod
    @transaction.atomic
    def create_graph_customer(request):
        """
        Возвращает массив, состоящий из дат графика расчета
        """
        input_data = JSONParser().parse(request)
        
        ku_id = input_data.get('ku_id')
        ku_instance = KuCustomer.objects.get(ku_id=ku_id)
        graph_exists = ku_instance.graph_exists

        if graph_exists:
            return Response({'error': 'Графики уже существуют для этого ku_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        graph_data_list = GraphProcessing.create_date_graph(period=ku_instance.period, date_start=ku_instance.date_start, 
                                                            date_end_initial=ku_instance.date_end, date_actual=ku_instance.date_actual)

        count_date_start = len([item['date_start'] for item in graph_data_list])

        sum_calc = ku_instance.pay_sum
        sum_bonus = round(sum_calc / count_date_start, 2)

        for date_range in graph_data_list:
            date_start = date_range['date_start']
            date_end = date_range['date_end']
            date_accrual = date_range['date_accrual']
            date_calc_time = timezone.now().date()

            if date_calc_time >= date_start:
                status_graph = 'Рассчитано'
            else:
                status_graph = 'Запланировано'
                sum_calc = 0
                sum_bonus = 0
            
            graph_customer = KuGraphCustomer.objects.create(
                ku=ku_instance,
                period=ku_instance.period,
                customer=ku_instance.customer,
                sum_calc=sum_calc,
                sum_bonus=sum_bonus,
                status=status_graph,
                date_start=date_start,
                date_end=date_end,
                date_accrual=date_accrual,
                date_calc=timezone.now()
            )
            
        if graph_data_list:  #при создании графиков заполнение поля "существование графика" в ку
            ku_instance.graph_exists = True
            ku_instance.save()
        
        return JsonResponse({"message": "Графики успешно созданы"}, status=status.HTTP_201_CREATED)
    