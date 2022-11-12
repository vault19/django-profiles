from django.contrib.auth.models import User
from django.forms import ModelForm, Form, IntegerField, TextInput, ImageField, BooleanField, FileField, DateField
from django.utils.translation import gettext_lazy as _

from profiles.models import Address, Profile, Membership


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]  # Temporarily removed email. Need a way to confirm email!


class SchoolForm(Form):
    school_id = IntegerField()


class ProofForm(ModelForm):
    class Meta:
        model = Membership
        fields = ["proof"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'address', 'country', 'metadata', 'header_image')


class UpdateSchoolsCVTIForm(Form):
    cvti_file = FileField(
        required=False,
        label="Register ŠaŠZ z https://crinfo.iedu.sk/risportal/register/",
    )
    store_changes_in_db = BooleanField(required=False, label='Store changes in DB (when unchecked, DB is not changed)')


class UpdateSchoolsINEKOForm(Form):
    file_zoznam_skol = FileField()
    file_udaje = FileField()
    file_doplnujuce_udaje = FileField()
    file_percentily = FileField()
    file_celkove_hodnotenie = FileField()
    file_polrocne_hodnotenie = FileField()
    file_cvc = FileField()
    date_of_data_collection = DateField()
