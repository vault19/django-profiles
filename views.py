from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect


from profiles.models import Address
from profiles.forms import PasswordChangingForm


# Create your views here.

def my_profile(request):
    return render(request, 'profiles/my_profile.html', {})

# TODO change messages into slovak language
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Vaše heslo bolo úspešne zmenené!')
            return redirect('change_password')
        else:
            messages.error(request, 'Opravte chybu nižšie, prosím!')
    else:
        form = PasswordChangingForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})


