from django.db import models


class Car(models.Model):
    number = models.SlugField(max_length=8, allow_unicode=True, unique=True)
    mark = models.CharField(max_length=50, db_index=True)
    model = models.CharField(max_length=80, db_index=True)
    year = models.IntegerField()

    user_name = models.CharField(max_length=80, db_index=True)
    user_number = models.CharField(max_length=15, db_index=True)

    def __str__(self):
        return f'User: {self.user_name}|Number: {self.number}'


class Repair(models.Model):
    id_car = models.ForeignKey("Car", on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
