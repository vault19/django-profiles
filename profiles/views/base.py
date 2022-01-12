import datetime

from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from profiles.forms import AddressForm, UserProfileForm, SchoolForm, ProfileForm
from profiles.models import School, Membership


@login_required
def full_profile(request):
    user = get_object_or_404(User, id=request.user.pk)

    user_form = UserProfileForm(instance=user)
    profile_form = ProfileForm(instance=user.profile)
    address_form = AddressForm(instance=user.profile.address)

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            user_form = UserProfileForm(request.POST, instance=user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                messages.success(request, _("Your profile has been saved."))
                return redirect("profile")

        if 'save_address' in request.POST:
            address_form = AddressForm(request.POST, instance=user.profile.address)

            if address_form.is_valid():
                address = address_form.save()
                user.profile.address = address
                user.profile.save()

                messages.success(request, _("Your address has been saved."))
                return redirect("profile")

        if 'save_school' in request.POST:
            membership_form = SchoolForm(request.POST)

            if membership_form.is_valid():
                school_id = membership_form.cleaned_data['school_id']
                school = School.objects.get(id=school_id)

                memberships = Membership.objects.filter(user=request.user)

                if memberships.count() == 0:
                    m = Membership(user=request.user, school=school, effective_from=datetime.datetime.now())
                    m.save()
                else:
                    for membership in memberships.all():
                        if membership.replaced_by is None and membership.school != school:
                            m = Membership(user=request.user, school=school, effective_from=datetime.datetime.now(),
                                           replaced_by=None)
                            m.save()

                            membership.effective_to = datetime.datetime.now()
                            membership.replaced_by = m
                            membership.save()
                            break

                messages.success(request, _("Your school has been saved."))
                return redirect("profile")

    context = {
        "breadcrumbs": [
            {
                "title": _("My Profile"),
            },
        ],
        "user_form": user_form,
        "profile_form": profile_form,
        "address_form": address_form,
    }

    return render(request, 'profiles/full_profile.html', context=context)


@login_required
def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profiles/public_profile.html', context={'user': user})
