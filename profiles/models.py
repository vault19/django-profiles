from django.conf import settings
from django.db import models
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
    street = models.CharField(max_length=250, verbose_name=_("Street"))
    city = models.CharField(max_length=250, verbose_name=_("City"))
    postal_code = models.CharField(max_length=250, verbose_name=_("Postal code"))
    country = models.CharField(max_length=2, verbose_name=_("Country"), choices=COUNTRY, default='SK')

    def __str__(self):
        return f"{self.street}, {self.city} {self.postal_code} {self.country}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, verbose_name=_("Phone"), blank=True, null=True)
    gender = models.CharField(max_length=1, verbose_name=_("Gender"), blank=True, null=True, choices=GENDER)
    account_type = models.CharField(max_length=2, verbose_name=_("Account type"), blank=True, null=True,
                                    choices=ACCOUNT_TYPE)
    about = models.TextField(blank=True, null=True, verbose_name=_("About me"))
    metadata = models.JSONField(blank=True, null=True, verbose_name=_("Metadata"),
                                help_text=_("Metadata about user."))
    country = models.CharField(blank=True, null=True, max_length=2, choices=COUNTRY, default='SK',
                               verbose_name=_("Country"))

    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class School(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"),
                                   help_text=_('Brief description about school.'))
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', blank=True)
    district = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("District"))
    region = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Region"))
    founder = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Founder"))
    school_type = models.CharField(max_length=50, verbose_name=_("School type"), blank=True, null=True)
    gps_x = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("GPS X"))
    gps_y = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("GPS Y"))
    school_code = models.CharField(max_length=50, verbose_name=_("School code"), blank=True, null=True)
    ineko_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Ineko ID"))
    underprivileged = models.IntegerField(blank=True, null=True, verbose_name=_("Unprivileged"))
    mail = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Email"))
    mail2 = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Email 3"))
    mail3 = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Email 3"))
    website = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Website"))

    def __str__(self):
        return f"{self.name} – {self.address} ({self.school_type})"


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    effective_from = models.DateField(blank=True, null=True, verbose_name=_("Effective from"))
    effective_to = models.DateField(blank=True, null=True, verbose_name=_("Effective to"))
    replaced_by = models.ForeignKey('Membership', blank=True, null=True, on_delete=models.CASCADE, default=None,
                                    verbose_name=_("Replaced by"))

    def __str__(self):
        return f"{self.school}: {self.user}"
