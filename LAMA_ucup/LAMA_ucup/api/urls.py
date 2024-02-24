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

    path('entitieslist/', EntitiesListView.as_view()),

    path('included_product_list/', IncludedProductsListView.as_view()),
    path('included_invoice_list/', IncludedInvoiceListView.as_view()),

    path('kulist/', KuListView.as_view()),
    path('ku/<str:pk>/', KuAPIUpdate.as_view()),
    path('kudetail/<str:pk>/', KuDetailView.as_view()),
    path('ku_create/', ku_create),

    path('included_condition_create/', included_products_create),  
    path('included_conditions_list/', IncludedСonditionListView.as_view()),  
    path('included_condition_detail/<int:pk>/', IncludedProductsView.as_view()),

    path('graphlist/', GraphListView.as_view()), 
    path('graphdetail/<int:pk>/', GraphDetailView.as_view()),
    path('create_graph/', create_graph, name='create-graph'),

    path('productslist/', ProductsListView.as_view()),
    path('productsfilter', products_filter, name ='products_filter'),

    path('venddoclist/', VendDocListView.as_view()),

    path('vendorlist/', VendorsListViewSet.as_view(actions={'get': 'list'}), name='vendor-list'),
    path('vendorfilter/', VendorsNameFilterView.as_view()),
    #path('vendorlist1', VendorsListView.as_view()),
    
    path('classifierlist',  ClassifierListView.as_view()),
    path('brandlist/', BrandClassifierListView.as_view()),

    path('me/', me_view),
]
