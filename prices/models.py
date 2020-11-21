from django.db import models
from django_cte import CTEManager


class PropertySale(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ("D", "Detached"),
        ("S", "Semi-Detached"),
        ("T", "Terraced"),
        ("F", "Flats/Maisonettes"),
        ("O", "Other"),
    )
    objects = CTEManager()

    price = models.IntegerField()
    date_of_transfer = models.DateTimeField()
    postcode = models.CharField(max_length=8)
    property_type = models.CharField(choices=PROPERTY_TYPE_CHOICES, max_length=1)
