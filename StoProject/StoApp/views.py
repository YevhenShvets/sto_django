from django.shortcuts import render, Http404, HttpResponse, redirect
from .models import *
import datetime
from django.views.generic import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    search_data = get_search_data()
    context = {
        'search_data': search_data
    }

    return render(request, 'StoApp/base_sto_app.html', context=context)


@login_required
def search_google(request, number):
    google_link = 'https://www.google.com/search?q='

    value = request.POST['input_value']
    car = Car.objects.get(number__iexact=number)

    car_data = f'+{car.mark}+{car.model}+{car.year}'
    return redirect(google_link+value+car_data)


@login_required
def calculation(request, number):
    if request.method == 'POST':
        id_calculation = request.POST['id_calculation']
        print('\n\n\n', request.POST)
        calc = Calculation.objects.get(id=id_calculation)
        calc.is_active = False
        calc.save()

    return redirect('info_number', number=number)


class CarCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = CarForm()
        search_data = get_search_data()

        return render(request, 'StoApp/create_form.html', context={'form': form, 'search_data': search_data})

    def post(self, request):
        car = CarForm(request.POST)
        if car.is_valid():
            car.cleaned_data['number'] = str(car.cleaned_data['number']).upper()
            new_car = car.save()
            return redirect('info_number', new_car.number)
        return render(request, 'StoApp/create_form.html', context={'form': car, 'search_data': get_search_data()})


class CarInfo(LoginRequiredMixin, View):
    def get(self, request, number):
        try:
            if not number:
                raise Http404("Автомобіля не існує")
            car = Car.objects.get(number__iexact=number.upper())
        except Car.DoesNotExist:
                raise Http404("Автомобіля не існує")
        repairs = Repair.objects.filter(id_car=car)

        # lastdate
        if repairs:
            d = repairs[len(repairs)-1].date
            lastdate = datetime(d.year, d.month, d.day).strftime("%d.%m.%Y")
        else:
            lastdate = datetime.now().strftime("%d.%m.%Y")

        # create rozrax items
        roz_items = get_roz_items()

        # create types repair
        types = [t.type for t in repairs]
        types = set(types)

        # create search data string
        search_data = get_search_data()

        # create context
        context = {
            'car': car,
            'repairs': repairs,
            'repairs_types': types,
            'search_data': search_data,
            'roz_items': roz_items,
            'last_date': lastdate

        }

        return render(request, 'StoApp/car_info.html', context=context)


class RepairCreate(LoginRequiredMixin, View):
    def get(self, request, number):
        form = RepairForm()
        car = Car.objects.get(number__iexact=number.upper())
        repairs = Repair.objects.filter(id_car=car)
        types = [t.type for t in repairs]
        types = set(types)
        return render(request, 'StoApp/create_repair.html', context={'form': form, 'types': types, 'car': car, 'search_data': get_search_data()})

    def post(self, request, number):
        repair = RepairForm(request.POST)
        is_calculation = request.POST.get('calculation')
        if repair.is_valid():
            car = Car.objects.get(number__iexact=number)
            new_repair = repair.save(commit=False)
            new_repair.id_car = car
            rep = new_repair.save()

            # add to calculation
            if is_calculation:
                is_create = True
                calc = Calculation.objects.filter(is_active=True)
                for c in calc:
                    if c.id_car == car:
                        is_create = False
                if is_create:
                    c = Calculation.objects.create(id_car=car, is_active=True)
                    ci = CalculationItem.objects.create(id_calculation=c, id_repair=new_repair)
                else:
                    c = Calculation.objects.get(id_car=car)
                    ci = CalculationItem.objects.create(id_calculation=c, id_repair=new_repair)

            return redirect('info_number', number)
        return render(request, 'StoApp/create_repair.html', context={'form': repair, 'search_data': get_search_data()})


def get_roz_items():
    rez = []
    calcul = Calculation.objects.filter(is_active=True)
    for c in calcul:
        user_name = c.id_car.user_name
        user_name+=" | "+c.id_car.number
        sum = 0
        repairs = []
        c_items = CalculationItem.objects.filter(id_calculation=c)
        for i in c_items:
            rem = i.id_repair
            repairs.append(rem)
            sum+=rem.price
        s = {
            "id_calculation": c.id,
            "user_name": user_name,
            "repairs": repairs,
            "price": sum
        }
        rez.append(s)
    return rez


def get_search_data():
    cars = Car.objects.all()
    search_data = [str(car.number + ' | ' + car.user_name + ' | ' + car.mark + ' ' + car.model + ' | ' + car.user_number) for car in cars]
    return search_data
