from django.db import models

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    rating = models.CharField(max_length=20)
    description = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.name

