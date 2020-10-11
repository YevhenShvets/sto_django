from django.contrib import admin
from .models import *


admin.site.register(Car)
admin.site.register(Repair)
admin.site.register(Calculation)
admin.site.register(CalculationItem)
