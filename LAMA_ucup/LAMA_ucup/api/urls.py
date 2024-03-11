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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import *

app_name = 'LAMA_ucup'

urlpatterns = [
    path('classifiersTest/', ClassifierTestList.as_view()),
    path('classifiers_tree/',ClassifierTreeView.as_view()),

    path('entitiy_list/', EntityListView.as_view()),

    path('included_product_list/', IncludedProductListView.as_view()),
    path('included_invoice_list/', IncludedInvoiceListView.as_view()),

    path('ku_list/', KuListView.as_view()),
    path('ku/<str:pk>/', KuAPIUpdate.as_view()),
    path('ku_detail/<str:pk>/', KuDetailView.as_view()),
    path('ku_create/', create_ku, name='ku_create'),

    path('included_condition_create/', included_product_create),  
    path('included_condition_list/', IncludedСonditionListView.as_view()),  
    path('included_condition_detail/<int:pk>/', IncludedProductsView.as_view()),

    path('graph_list/', GraphListView.as_view()), 
    path('graph_detail/<int:pk>/', GraphDetailView.as_view()),
    path('graph_create/', create_graph_new, name='create-graph'),
    path('create_graph_new/', create_graph_new, name='create-graph-new'),

    path('product_list/', ProductsListView.as_view()),
    path('product_filter/', products_filter, name ='products_filter'),

    path('vend_doc_list/', VendDocListView.as_view()),

    path('vendor_list/', VendorsListViewSet.as_view(actions={'get': 'list'}), name='vendor-list'),
    path('vendor_filter/', VendorsNameFilterView.as_view()),
    
    path('classifier_list/',  ClassifierListView.as_view()),
    path('brand_list/', BrandClassifierListView.as_view()),

    path('me/', me_view),
]
