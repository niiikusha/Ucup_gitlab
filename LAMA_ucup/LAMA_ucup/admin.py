from django.contrib import admin
from .models import *

admin.site.register(Entities)
admin.site.register(AuthUser)
admin.site.register(Vendors)
admin.site.register(Products)
admin.site.register(ClassifierTest)
admin.site.register(Brandclassifier)
admin.site.register(Classifier)
admin.site.register(IncludedProducts)
admin.site.register(IncludedProductsList)
admin.site.register(Invoices)
admin.site.register(Ku)
admin.site.register(KuGraph)
admin.site.register(Venddoc)
admin.site.register(Venddoclines)

# Register your models here.
