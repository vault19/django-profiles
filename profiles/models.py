from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image

from profiles.validators import FileSizeValidator
from profiles import settings as profile_settings

ACCOUNT_TYPE = (
    ('PT', _('Primary School Teacher')),
    ('ST', _('Secondary School Teacher')),
    ('S', _('Student')),
    ('O', _('Enthusiast')),
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
    ('XX', _('Other (insert into note)')),
)


class Address(models.Model):
    street = models.CharField(max_length=250, verbose_name=_("Street"))
    city = models.CharField(max_length=250, verbose_name=_("City"))
    postal_code = models.CharField(max_length=250, verbose_name=_("Postal code"))
    country = models.CharField(max_length=2, verbose_name=_("Country"), choices=COUNTRY, default='SK')
    note = models.CharField(max_length=250, verbose_name=_("Address note"), blank=True, null=True)

    def __str__(self):
        return f"{self.street}, {self.city} {self.postal_code} {self.country}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, verbose_name=_("Phone"), blank=True, null=True)
    header_image = models.ImageField(verbose_name=_("Header image"), blank=True, null=True, upload_to='profile-headers',
                               validators=[
                                   FileExtensionValidator(["jpg", "jpeg", "png"]),
                                   FileSizeValidator(profile_settings.HEADER_MAX_FILE_SIZE),
                               ])
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.RESTRICT)
    gender = models.CharField(max_length=1, verbose_name=_("Gender"), blank=True, null=True, choices=GENDER)
    account_type = models.CharField(max_length=2, verbose_name=_("Account type"), blank=True, null=True,
                                    choices=ACCOUNT_TYPE)
    avatar = models.ImageField(verbose_name=_("Avatar"), blank=True, null=True, upload_to='avatars',
                               validators=[
                                   FileExtensionValidator(["jpg", "jpeg", "png"]),
                                   FileSizeValidator(profile_settings.AVATAR_MAX_FILE_SIZE),
                               ])
    about = models.TextField(blank=True, null=True, verbose_name=_("About me"))
    metadata = models.JSONField(blank=True, null=True, verbose_name=_("Metadata"),
                                help_text=_("Metadata about user."))
    country = models.CharField(blank=True, null=True, max_length=2, choices=COUNTRY, default='SK',
                               verbose_name=_("Country"))
    metadata = models.JSONField(
        verbose_name=_("Metadata"), blank=True, null=True, help_text=_("Metadata about user.")
    )

    def __str__(self):
        return f"{self.user}"

    def save(self, *args, **kwargs):
        # TODO: process header image for public profile

        if self.avatar:
            super().save(*args, **kwargs)

            img = Image.open(self.avatar.path)

            if img.height > profile_settings.AVATAR_MAX_HEIGHT or img.width > profile_settings.AVATAR_MAX_WIDTH:
                output_size = (profile_settings.AVATAR_MAX_WIDTH, profile_settings.AVATAR_MAX_HEIGHT)
                img.thumbnail(output_size)
                img.save(self.avatar.path, quality=profile_settings.AVATAR_DEFAULT_QUALITY)
        else:
            super().save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class School(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"),
                                   help_text=_('Brief description about school.'))
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', blank=True)
    district = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("District"))
    region = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Region"))
    founder = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Founder"))
    school_type = models.CharField(max_length=50, verbose_name=_("School type"), blank=True, null=True)
    gps_x = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("GPS X"))
    gps_y = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("GPS Y"))
    school_code = models.CharField(max_length=50, verbose_name=_("KODSKO"), blank=True, null=True)
    edu_id = models.CharField(max_length=50, verbose_name=_("EDUID"), blank=True, null=True)
    ineko_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("INEKO ID"))
    underprivileged = models.IntegerField(blank=True, null=True, verbose_name=_("Unprivileged"))
    number_of_students = models.IntegerField(blank=True, null=True, verbose_name=_("Number of Students"))
    mail = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Email"))
    mail2 = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Email 3"))
    mail3 = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Email 3"))
    website = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Website"))

    timestamp_added = models.DateTimeField(verbose_name=_("Added"), auto_now_add=True)
    timestamp_modified = models.DateTimeField(verbose_name=_("Modified"), auto_now=True)

    def __str__(self):
        return f"{self.name} – {self.address} ({self.school_type})"


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.RESTRICT)
    effective_from = models.DateField(blank=True, null=True, verbose_name=_("Effective from"))
    effective_to = models.DateField(blank=True, null=True, verbose_name=_("Effective to"))
    replaced_by = models.ForeignKey('Membership', blank=True, null=True, on_delete=models.RESTRICT, default=None,
                                    verbose_name=_("Replaced by"))
    proof = models.ImageField(verbose_name=_("Proof"), blank=True, null=True, upload_to='profile-school-proof',
                               validators=[
                                   FileExtensionValidator(["jpg", "jpeg", "png"]),
                                   FileSizeValidator(profile_settings.HEADER_MAX_FILE_SIZE),
                               ])
    verified = models.BooleanField(verbose_name=_("Verified"), default=False)

    def __str__(self):
        return f"{self.school}: {self.user}"
