from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect


from profiles.models import Address
from profiles.forms import PasswordChangingForm


# Create your views here.


# TODO change messages into slovak language
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please, correct the error below.')
    else:
        form = PasswordChangingForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})


