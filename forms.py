from django.contrib.auth.forms import PasswordChangeForm


class PasswordChangingForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None

        self.fields['old_password'].label = "Staré heslo"
        self.fields['new_password1'].label = "Nové heslo"
        self.fields['new_password2'].label = "Potvrďte nové heslo"
