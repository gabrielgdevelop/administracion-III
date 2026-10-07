from django.db import models
from apps.catalogs.models.month import Month

class Week(models.Model):
    number = models.CharField(max_length=20, unique=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='weeks')

    class Meta:
        verbose_name = "Semana"
        verbose_name_plural = "Semanas"
        db_table = "week"

    def __str__(self):
        return f"{self.name} ({self.month.name} - {self.month.year.name})"  