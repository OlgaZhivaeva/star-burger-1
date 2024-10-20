from django.db import models
from django.core.validators import MinValueValidator


class Geocoords(models.Model):
    address = models.CharField(
        verbose_name='адрес',
        max_length=200,
        blank=True,
        unique=True
    )
    lon = models.DecimalField(
        verbose_name='долгота',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True
    )
    lat = models.DecimalField(
        verbose_name='широта',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True
    )
    request_date = models.DateTimeField(
        verbose_name='дата запроса',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'координаты'
        verbose_name_plural = 'координаты'

    def __str__(self):
        return self.address
