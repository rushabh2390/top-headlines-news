from django.db import models
from country.models import Country
import hashlib

# Create your models here.


class News(models.Model):
    title = models.TextField()
    author = models.TextField(blank=True, null=True)
    publisher_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    news_url = models.CharField(blank=True, null=True)
    image_url = models.CharField(blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True)
    hashvalue = models.CharField(max_length=300)
    last_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Set the custom database table name
        db_table = 'news'

    def save(self, *args, **kwargs):
        # Calculate the hash if it's not set
        if not self.hashvalue:
            combined_string = f"{self.title}{self.publisher_date}"
            sha256_hash = hashlib.sha256()
            sha256_hash.update(combined_string.encode('utf-8'))
            self.hashvalue = sha256_hash.hexdigest()
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
