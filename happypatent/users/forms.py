from django import forms
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User


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


class UserProfileModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id_number', 'gender',
                  'county', 'address', 'home_number', 'mobile_number',
                  'office_number', 'spouse_name', 'education', 'experience',
                  'remarks', 'profile_pic']

