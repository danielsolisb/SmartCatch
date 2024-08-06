from smartcatch.settings import MEDIA_ROOT, BASE_DIR, STATIC_URL, MEDIA_URL
from django.db import models

from django.db.models.fields import EmailField
from django.contrib.auth.models import BaseUserManager, AbstractUser, AbstractBaseUser
from django.db.models.query import FlatValuesListIterable
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import ImageField
#from CoreApps.Stations.models import Station

import datetime

# Create your models here.

class User(AbstractUser):
    options=[
        ['industrial', 'Industrial'],
        ['agricola', 'Agricola'],
        ['avicola', 'Avicola'],
    ]
    id_ced          = models.CharField(max_length=20, verbose_name="ID Number", unique=True, null=True, blank=True)
    address         = models.CharField(max_length=150, verbose_name="Address", null=True, blank="True") 
    degree_title    = models.CharField(max_length=20, verbose_name="Degree title", null=True, blank=True)
    telephone       = models.CharField(max_length=50, verbose_name="Telephone",blank=True, null=True)
    country         = models.CharField(max_length=30, verbose_name="Country", null=False, blank=False)
    company         = models.CharField(max_length=50, verbose_name="Company",blank=True, null=True)
    email           = models.EmailField(unique=True, max_length=70, null=False, blank=False)
    categorie       = models.CharField(choices=options, max_length=50, blank=False, null=True)

    #StationID       = models.ForeignKey(Station, null=True, blank=True, default=None, on_delete=CASCADE)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'password']
    def __str__(self):
        return self.get_full_name()
    
    def get_user_login(self):
        return str(self.pk)
    
    def get_Company(self):
        #print(self.establecimiento)
        return self.company
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'