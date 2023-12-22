from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.TextField()
    country_code = models.TextField()

    class Meta:
        # Set the custom database table name
        db_table = 'country'
    
    
    def __str__(self):
        return self.country_name