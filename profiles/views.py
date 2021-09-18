from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from profiles.forms import PasswordChangingForm, AddressForm, UserProfileForm, SchoolForm, ProfileForm


# Create your views here.
@login_required
def my_profile(request):
    user = get_object_or_404(User, id=request.user.pk)

    user_form = UserProfileForm(instance=user)
    profile_form = ProfileForm(instance=user.profile)
    address_form = AddressForm(instance=user.profile.address)
    membership_form = SchoolForm()

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            user_form = UserProfileForm(request.POST, instance=user)
            profile_form = ProfileForm(request.POST, instance=user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

        if 'save_address' in request.POST:
            address_form = AddressForm(request.POST, instance=user.profile.address)

            if address_form.is_valid():
                address_form.save()

        if 'save_membership' in request.POST:
            membership_form = SchoolForm(request.POST)

            if membership_form.is_valid():
                membership_form.save()

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "address_form": address_form,
        "membership_form": membership_form,
    }

    return render(request, 'profiles/profile.html', context=context)


# TODO change messages into slovak language
@login_required
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
    return render(request, 'profiles/password_change_form.html', {'form': form})
