import datetime

from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from profiles.forms import AddressForm, UserProfileForm, SchoolForm, ProfileForm
from profiles.models import School, Membership


@login_required
def edit_profile(request):
    user = get_object_or_404(User, id=request.user.pk)
    context = {
        "post_url": request.GET.get("post_url", reverse("edit_address")),
        "modal_icon": "far fa-envelope",
        "modal_title": _("Edit Address"),
        "modal_action": _("Save Address"),
    }

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            context["message"] = _("Your profile has been saved.")
            # messages.success(request, _("Your profile has been saved."))
            # return redirect("profile")
        else:
            context['form'] = user_form
            context['form2'] = profile_form
    else:
        context['form'] = UserProfileForm(instance=user)
        context['form2'] = ProfileForm(instance=user.profile)

    return render(request, 'profiles/ajax/form_generic.html', context=context)


@login_required
def edit_address(request):
    user = get_object_or_404(User, id=request.user.pk)
    context = {
        "post_url": request.GET.get("post_url", reverse("edit_address")),
        "modal_icon": "far fa-envelope",
        "modal_title": _("Edit Address"),
        "modal_action": _("Save Address"),
    }

    if request.method == "POST":
        form = AddressForm(request.POST, instance=user.profile.address)

        if form.is_valid():
            address = form.save()
            user.profile.address = address
            user.profile.save()

            context["message"] = _("Your address has been saved.")
            # messages.success(request, _("Your address has been saved."))
            # return redirect("profile")
        else:
            context["form"] = form
    else:
        form = AddressForm(instance=user.profile.address)
        context["form"] = form

    return render(request, "profiles/ajax/form_generic.html", context)


@login_required
def search_school(request):
    context = {}

    if request.method == 'POST' and 'search' in request.POST:
        schools = School.objects.filter(Q(name__icontains=request.POST['search']) |
                                        Q(address__street__icontains=request.POST['search']) |
                                        Q(address__city__icontains=request.POST['search']) |
                                        Q(school_code__icontains=request.POST['search'])
                                        ).filter().all()

        context['schools'] = schools

    return render(request, 'profiles/ajax/school_search.html', context=context)
