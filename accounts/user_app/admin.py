from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Returns)
admin.site.register(models.Staffs)
admin.site.register(models.Products)
admin.site.register(models.Expences)
admin.site.register(models.Sales)