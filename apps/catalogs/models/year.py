from django.db import models

class Year(models.Model):
    name = models.CharField(max_length=4, unique=True)

    class Meta:
        verbose_name = "Año"
        verbose_name_plural = "Años"
        db_table = "year"

    def __str__(self):
        return self.name