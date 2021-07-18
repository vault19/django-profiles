from django.conf import settings
from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=250)
    number = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=250)
    country = models.CharField(max_length=250)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class School(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(help_text='Brief description about school.')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership')


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    effective_from = models.DateField()
    effective_from = models.DateField()
    invite_reason = models.CharField(max_length=64)