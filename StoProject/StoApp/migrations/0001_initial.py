# Generated by Django 3.1.2 on 2020-10-02 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SlugField(allow_unicode=True, max_length=8, unique=True)),
                ('mark', models.CharField(db_index=True, max_length=50)),
                ('model', models.CharField(db_index=True, max_length=80)),
                ('year', models.IntegerField(max_length=4)),
                ('user_name', models.CharField(db_index=True, max_length=80)),
                ('user_number', models.CharField(db_index=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('id_car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoApp.car')),
            ],
        ),
    ]
