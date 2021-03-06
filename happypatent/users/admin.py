from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, CalendarEvent


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    user_profile_fields = ('id_number', 'gender', 'county', 'address', 'home_number',
                           'mobile_number', 'office_number', 'spouse_name', 'education',
                           'experience', 'remarks', 'profile_pic')
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
            ('User Profile', {'fields': user_profile_fields}),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'first_name', 'last_name', 'is_superuser')
    search_fields = ['first_name', 'last_name', 'id_number']


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    pass
