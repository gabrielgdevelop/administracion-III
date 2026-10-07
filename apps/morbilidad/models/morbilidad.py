# apps/morbilidad/models/morbilidad.py
from django.db import models
from apps.catalogs.models.year import Year
from apps.catalogs.models.month import Month
from apps.catalogs.models.week import Week
from apps.morbilidad.models.detail_morbilidad import DetailMorbilidad

class Morbilidad(models.Model):
    ESTADOS = (
        ('Pendiente', 'Pendiente'),
        ('Validado', 'Validado'),
        ('Reportado', 'Reportado'),
    )
    morbilidad_detalle = models.ForeignKey(DetailMorbilidad, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    class Meta:
        db_table = 'morbilidad'

    def __str__(self):
        return f"Registro {self.id} - {self.estado}"