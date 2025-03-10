# Generated by Django 3.2.15 on 2024-10-20 10:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Geocoords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, unique=True, verbose_name='адрес')),
                ('lon', models.DecimalField(blank=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='долгота')),
                ('lat', models.DecimalField(blank=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='широта')),
                ('request_date', models.DateTimeField(auto_now_add=True, verbose_name='дата запроса')),
            ],
        ),
    ]
