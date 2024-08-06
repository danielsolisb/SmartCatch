from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import BaseIterable
from django.utils.translation import templatize
from datetime import date, timedelta

class Station(models.Model):
    user_ID     =    models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True)
    name        =    models.CharField(max_length=50, blank=True, null=True, verbose_name='Estación')
    address     =    models.CharField(max_length=50, blank=False, null=True)
    telephone   =    models.IntegerField(blank=False, null=False)
    coordinates =    models.CharField(max_length=100, blank=False, null=True)
    


    def __str__(self):
        return self.name