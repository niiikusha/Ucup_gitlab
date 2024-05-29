from .models import Ku
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

class ContractProcessing:
    @staticmethod
    def create_name_contract(request):
        input_data = JSONParser().parse(request)
        contract_name = ''
        response_data = {}

        vendor_name = input_data.get('vendor_name')
        ku_type = input_data.get('ku_type')
        provider_list = input_data.get('provider_list')
        brand_list = input_data.get('brand_list')

        if ku_type == 'Услуга':
            contract_name = 'МУ_'
        elif ku_type == 'Ретро-бонус':
            contract_name = 'ВЗ_'
        
        contract_name += vendor_name + '_'

        contract_name += ",".join(provider_list) + '_' + ",".join(brand_list)
        response_data['name'] = contract_name

        return JsonResponse(response_data, status=status.HTTP_200_OK)