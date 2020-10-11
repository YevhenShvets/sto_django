from django.db import models
from django.shortcuts import  reverse


class Car(models.Model):
    number = models.SlugField(max_length=8, allow_unicode=True, unique=True, verbose_name='Номер авто')
    mark = models.CharField(max_length=50, db_index=True, verbose_name='Марка авто')
    model = models.CharField(max_length=80, db_index=True, verbose_name='Модель авто')
    year = models.IntegerField(verbose_name='Рік')

    user_name = models.CharField(max_length=80, db_index=True, verbose_name="Ім'я власника")
    user_number = models.CharField(max_length=17, db_index=True, verbose_name='Телефон власника')

    def __str__(self):
        return f'User: {self.user_name}|Number: {self.number}'


class Repair(models.Model):
    id_car = models.ForeignKey("Car", on_delete=models.CASCADE)
    type = models.CharField(max_length=100, verbose_name='Тип ремонту')
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.FloatField(verbose_name='Ціна')
    date = models.DateTimeField(verbose_name='Дата')

    def __str__(self):
        return self.description

    def get_create_url(self):
        return reverse('create_repair', kwargs={'number': self.id_car.number})


class Calculation(models.Model):
    id_car = models.ForeignKey("Car", on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return str(self.id_car)


class CalculationItem(models.Model):
    id_calculation = models.ForeignKey("Calculation", on_delete=models.CASCADE)
    id_repair = models.ForeignKey("Repair", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_calculation)

