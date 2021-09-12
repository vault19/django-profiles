from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime

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
    number = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=250)
    country = models.CharField(max_length=2, choices=COUNTRY, default='SK')

    def __str__(self):
        return f"{self.street} {self.number}, {self.city} {self.postal_code} {self.country}"


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


class School(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True, help_text=_('Brief description about school.'))
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    founder = models.CharField(max_length=50, blank=True, null=True)
    school_type = models.CharField(max_length=50, blank=True, null=True)
    gps_x = models.CharField(max_length=50, blank=True, null=True)
    gps_y = models.CharField(max_length=50, blank=True, null=True)
    school_code = models.CharField(max_length=50, blank=True, null=True)
    ineko_id = models.CharField(max_length=50, blank=True, null=True)
    underprivileged = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} – {self.address}"


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # effective_from = models.DateField(default=datetime.date.today())
    effective_from = datetime.date
    effective_to = models.DateField(blank=True, null=True)

    def __str__(self):
        effective_to = self.effective_to if self.effective_to else datetime.date.today()
        return f"{self.school}: {self.user} ({effective_to - self.effective_from})"
