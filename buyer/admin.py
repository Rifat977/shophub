from django.contrib import admin
from .models import Invoice, Purchase

# Register your models here.

admin.site.register(Invoice)
admin.site.register(Purchase)