from django.contrib.auth.models import Permission, User
from django.db import models


class Brewery(models.Model):
    user = models.ForeignKey(User, default=1)
    brew_name = models.CharField(max_length=50)
    brew_location = models.CharField(max_length=70)
    brew_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.brew_name


class Beer(models.Model):
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    beer_name = models.CharField(max_length=250)
    beer_type = models.CharField(max_length=20)
    # beer_description = models.TextField(default='')
    beer_image = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.beer_name
