from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from profiles.models import Address


class PasswordChangingForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None

        self.fields['old_password'].label = _("Old password")
        self.fields['new_password1'].label = _("New Password")
        self.fields['new_password2'].label = _("Confirm new password")


class AddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        self.fields['street'].label = _("Street")
        self.fields['number'].label = _("Number")
        self.fields['city'].label = _("City")
        self.fields['postal_code'].label = _("Postal code")
        self.fields['country'].label = _("Country")

    class Meta:
        model = Address
        fields = "__all__"

