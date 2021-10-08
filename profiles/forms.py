from django.contrib.auth.models import User
from django.forms import ModelForm, Form, IntegerField

from profiles.models import Address, Profile


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class SchoolForm(Form):
    school_id = IntegerField()


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'address', 'country')
