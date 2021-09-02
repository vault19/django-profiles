from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from profiles.models import Address, Profile
from profiles.forms import PasswordChangingForm, AddressForm, UserProfileForm


# Create your views here.
@login_required
def my_profile(request):
    profile_info = Profile.objects.get(user=request.user.pk)
    instance = get_object_or_404(Address, id=profile_info.pk)
    form = AddressForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()

    user_instance = get_object_or_404(User, id=request.user.pk)
    user_form = UserProfileForm(request.POST or None, instance=user_instance)

    if user_form.is_valid():
        user_form.save()

    return render(request, 'profiles/my_profile.html', {"form": form, "user_form":user_form})


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
    return render(request, 'profiles/change_password.html', {'form': form})
