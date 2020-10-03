from django.shortcuts import render, HttpResponse
from .models import *
from django.views.generic  import View

def index(request):
    return render(request, 'StoApp/base_sto_app.html')


class CarInfo(View):
    def get(self, request, number):
        car = Car.objects.get(number__iexact=number.upper())
        repairs = Repair.objects.filter(id_car=car)

        # create types repair
        types = [t.type for t in repairs]

        context = {
            'car': car,
            'repairs': repairs,
            'repairs_types': types
        }

        return render(request, 'StoApp/car_info.html', context=context)

