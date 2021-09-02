from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from profiles.models import Address, Profile
from profiles.forms import PasswordChangingForm, AddressForm


# Create your views here.

def my_profile(request):
    profile_info = Profile.objects.get(user=request.user.pk)
    address = profile_info.address
    form = AddressForm(request.POST or None, instance=Address(street=address.street, number=address.number,
                                                              city=address.city, postal_code=address.postal_code,
                                                              country=address.country), auto_id=1)

    if form.is_valid():
        form.save()

    print("Profile info: ", profile_info.address.city)
    return render(request, 'profiles/my_profile.html', {"context": form, "keket": profile_info})


# TODO change messages into slovak language
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully changed!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Fix the error below, please!'))
    else:
        form = PasswordChangingForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})
