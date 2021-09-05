from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from profiles.models import Address, Membership, Profile


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

        self.description = _("Address")

    class Meta:
        model = Address
        fields = "__all__"


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].label = _("First name")
        self.fields["last_name"].label = _("Last name")
        self.fields["email"].label = _("Email")

        self.description = _("Personal")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class MembershipForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        self.fields["school"].label = _("School")

        self.description = _("School")

    class Meta:
        model = Membership
        fields = ["school"]


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        self.fields["phone_number"].label = _("Phone number:")

    class Meta:
        model = Profile
        fields = ["phone_number"]
