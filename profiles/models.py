import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

ACCOUNT_TYPE = (
    ('PT', _('Primary School Teacher')),
    ('ST', _('Secondary School Teacher')),
    ('S', _('Student')),
    ('P', _('Parent')),
    ('L', _('Lecturer')),
    ('O', _('Other')),
)

GENDER = (
    ('M', _('Male')),
    ('F', _('Female')),
)

COUNTRY = (
    ('SK', _('Slovakia')),
    ('CZ', _('Czechia')),
    ('HU', _('Hungary')),
    ('PL', _('Poland')),
)


class Address(models.Model):
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=250)
    country = models.CharField(max_length=2, choices=COUNTRY, default='SK')

    def __str__(self):
        return f"{self.street}, {self.city} {self.postal_code} {self.country}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER)
    account_type = models.CharField(blank=True, null=True, max_length=2, choices=ACCOUNT_TYPE)
    about = models.TextField(blank=True, null=True)
    country = models.CharField(blank=True, null=True, max_length=2, choices=COUNTRY, default='SK')

    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class School(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True, help_text=_('Brief description about school.'))
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', blank=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    founder = models.CharField(max_length=50, blank=True, null=True)
    school_type = models.CharField(max_length=50, blank=True, null=True)
    gps_x = models.CharField(max_length=50, blank=True, null=True)
    gps_y = models.CharField(max_length=50, blank=True, null=True)
    school_code = models.CharField(max_length=50, blank=True, null=True)
    ineko_id = models.CharField(max_length=50, blank=True, null=True)
    underprivileged = models.IntegerField(blank=True, null=True)
    mail = models.CharField(blank=True, null=True, max_length=100)
    mail2 = models.CharField(blank=True, null=True, max_length=100)
    mail3 = models.CharField(blank=True, null=True, max_length=100)
    website = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return f"{self.name} – {self.address} ({self.school_type})"


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    effective_from = models.DateField(blank=True, null=True)
    effective_to = models.DateField(blank=True, null=True)
    replaced_by = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.school}: {self.user}"
