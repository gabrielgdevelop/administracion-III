from django.db import models
from apps.catalogs.models.year import Year

class Month(models.Model):
    name = models.CharField(max_length=20, unique=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='months')

    class Meta:
        verbose_name = "Mes"
        verbose_name_plural = "Meses"
        db_table = "month"

    def __str__(self):
        return f"{self.name} ({self.year.name})"