from django import forms
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import SignupForm


class MySignupForm(SignupForm):
    first_name = forms.CharField(label=_("First_Name"),
                                 max_length=20,
                                 widget=forms.TextInput(
                                     attrs={'placeholder':
                                                _('First Name'),
                                            }
                                     )
                                 )
    last_name = forms.CharField(label=_("Last_Name"),
                                 max_length=20,
                                 widget=forms.TextInput(
                                     attrs={'placeholder':
                                                _('Last Name'),
                                            }
                                     )
                                )

    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        field_order = ['email', 'username', "first_name", 'last_name', 'password1', 'password2']


