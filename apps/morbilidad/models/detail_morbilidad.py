from django.db import models

class DetailMorbilidad(models.Model):
    cedula = models.CharField(max_length=20, verbose_name='Cédula')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    edad = models.IntegerField(verbose_name='Edad')
    diagnostico = models.TextField()
    fecha = models.DateField()

    class Meta:
        verbose_name = 'Detalle de Morbilidad'
        verbose_name_plural = 'Detalles de Morbilidad'
        db_table = 'detail_morbilidad'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.diagnostico}"