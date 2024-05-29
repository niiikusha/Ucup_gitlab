"""
URL configuration for LAMA_ucup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from .views import *

app_name = 'LAMA_ucup'

urlpatterns = [
    
    path('get_customer_dir_party/<str:pk>/', get_customer_dir_party), #выводит всех клиентов по dir party поставщика
    path('excluded_venddoc_detail/<int:pk>/', ExcludedVenddocView.as_view()),
    path('bonus_condition_detail/<int:pk>/', BonusConditionView.as_view()),

    path('official_detail/<int:pk>/', OfficialView.as_view()),
    path('official_customer_detail/<int:pk>/', OfficialCustomerView.as_view()),

    path('manager_detail/<int:pk>/', ManagerView.as_view()),

    path('classifiersTest/', ClassifierTestList.as_view()),
    path('classifier_tree/', ClassifierTreeView.as_view()),

    path('category_list/', CategoryListView.as_view()),

    path('entity_list/', EntityListView.as_view()),

    path('vendor_detail/<str:pk>/', VendorDetailView.as_view()),
    path('entity_detail/<str:pk>/', EntityDetailView.as_view()),

    path('kafka_process/',kafka_process, name='ku_create'),

    path('manager_list/', ManagerListView.as_view()),
    path('manager_ku/', ManagerKuListView.as_view()),
    path('manager_ku_customer/', ManagerKuCustomerListView.as_view()),
    path('manager_ku_detail/<str:pk>/', ManagerKuDetailView.as_view()),
    path('manager_ku_customer_detail/<str:pk>/', ManagerKuCustomerDetailView.as_view()),

    path('official_create/', OfficialListView.as_view()),
    path('official_customer_create/', OfficialCustomerListView.as_view()),

    path('included_product_list/', IncludedProductListView.as_view()),
    path('included_invoice_list/', IncludedInvoiceListView.as_view()),

    path('excluded_product_list/', ExcludedProductListView.as_view()),

    path('bonus_condition/', BonusConditionList.as_view()),

    path('ku_list/', KuListView.as_view()),
    path('ku/<str:pk>/', KuAPIUpdate.as_view()),
    path('ku_detail/<str:pk>/', KuDetailView.as_view()),
    path('ku_create/', create_ku, name='ku_create'),
    
    path('ku_customer_create/', create_ku_customer, name='ku_create_customer'),
    path('ku_customer_detail/<str:pk>/', KuCustomerDetailView.as_view()),

    path('name_contact_create/', name_contact_create, name='name_contact_create'),

    path('excluded_venddoc_list_create/', ExcludedVenddocList.as_view()),
    path('excluded_venddoc_list_full/', ExcludedVenddocFullView.as_view()),

    path('included_condition_create/', included_products_create),  
    path('included_condition_list/', IncludedСonditionListView.as_view()),  
    path('included_condition_detail/<int:pk>/', IncludedProductView.as_view()),

    path('excluded_condition_create/', excluded_products_create),  
    path('excluded_condition_list/', ExcludedСonditionListView.as_view()),  
    path('excluded_condition_detail/<int:pk>/', ExcludedProductView.as_view()),

    path('graph_list/', GraphListView.as_view()), 
    path('graph_detail/<int:pk>/', GraphDetailView.as_view()),
    path('graph_words/<int:pk>/', GraphWordslView.as_view()),
    path('graph_create/', create_graph_new, name='create-graph'),
    path('graph_create_new/', create_graph_new, name='create-graph-new'),

    path('graph_create_customer/', create_graph_customer, name='create-graph-customer'),

    path('product_list/', ProductListView.as_view()),
    path('product_filter', products_filter, name ='products_filter'),

    path('vend_doc_list/', VendDocListView.as_view()),

    path('vendor_list/', VendorListViewSet.as_view(actions={'get': 'list'}), name='vendor-list'),
    path('vendor_filter/', VendorNameFilterView.as_view()),
    
    path('classifier_list/',  ClassifierListView.as_view()),
    path('brand_list/', BrandClassifierListView.as_view()),

    path('included_vendor_create/', IncludedVendorView.as_view()),
    path('included_vendor_detail/<int:pk>/', IncludedVendorDetailView.as_view()),
    path('included_vendor_customer_create/', IncludedVendorCustomerView.as_view()),
    path('included_vendor_customer_detail/<int:pk>/', IncludedVendorCustomeDetailView.as_view()),


    path('me/', me_view),

    #клиенты

    path('service_list/', ServiceListView.as_view()), #справочник оказываемых  услуг
    path('service_detail/<int:pk>/', ServiceDetailView.as_view()),

    path('article_list/', ArticleListView.as_view()), #справочник услуг
    path('article_detail/<int:pk>/', ArticleDetailView.as_view()),

    path('place_service_list/', PlaceServiceListView.as_view()), #места оказания услуг
    path('place_service_detail/<int:pk>/', PlaceDetailView.as_view()),

    path('price_list/', PriceListListView.as_view()), #прайс лист на оказываемые услуги
    path('price_list_detail/<int:pk>/', PriceListDetailView.as_view()),

    path('included_service_list/', IncludedServiceListView.as_view()), #прайс лист на оказываемые услуги
    path('included_service_detail/<int:pk>/', IncludedServiceDetailView.as_view()),
    path('customer_list/', CustomerListView.as_view()), #клиенты
    path('customer_detail/<str:pk>/', CustomerDetailView.as_view()),
    path('graph_customer_list/', KuGraphCustomerListView.as_view()), #график клиентов
    path('ku_customer_list/', KuCustomerListView.as_view()), #график клиентов
    path('graph_create_customer/', create_graph_customer, name='create-graph-customer'),
    path('graph_customer_detail/<int:pk>/', GraphCustomerDetailView.as_view()),

]
