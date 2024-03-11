from django.contrib import admin
from .models import *

admin.site.register(Entity)
admin.site.register(AuthUser)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(ClassifierTest)
admin.site.register(BrandClassifier)
admin.site.register(Classifier)
admin.site.register(IncludedCondition)
admin.site.register(IncludedProduct)
admin.site.register(Ku)
admin.site.register(KuGraph)
admin.site.register(VendDoc)
admin.site.register(VendDocLine)

# Register your models here.
