from django.contrib import admin
from .models import *

admin.site.register(Entity)
admin.site.register(AuthUser)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(ClassifierTest)
admin.site.register(Brandclassifier)
admin.site.register(Classifier)
admin.site.register(IncludedProduct)
admin.site.register(IncludedProductList)
admin.site.register(Ku)
admin.site.register(KuGraph)
admin.site.register(Venddoc)
admin.site.register(Venddoclines)

# Register your models here.
