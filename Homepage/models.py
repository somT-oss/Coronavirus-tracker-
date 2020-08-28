from django.db import models

class CountryName(models.Model):
    country_name = models.CharField(max_length=35)

    def __str__(self):
        return self.country_name
    
    class Meta:
        verbose_name_plural = "countries"

# Create your models here.
