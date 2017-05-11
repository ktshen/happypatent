from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class BaseProfileModel(models.Model):
    GENDER_CHOICE = (
        ('m', _('Male')),
        ('f', _('Female'))
    )

    id_number = models.CharField(_('ID Number'),
                                 max_length=10,
                                 blank=True,
                                 )

    gender = models.CharField(_('Gender'),
                              choices=GENDER_CHOICE,
                              max_length=10,
                              default='m')

    county = models.CharField(_('County/City'),
                              max_length=30,
                              blank=True)

    address = models.CharField(_('Address'),
                               max_length=100,
                               blank=True)

    home_number = models.CharField(_('Home Phone Number'),
                                   max_length=15,
                                   blank=True)

    mobile_number = models.CharField(_('Mobile'),
                                     max_length=15,
                                     blank=True)

    office_number = models.CharField(_('Office Number'),
                                     max_length=15,
                                     blank=True)

    spouse_name = models.CharField(_('Spouse Name'),
                                   max_length=50,
                                   blank=True)

    education = models.TextField(_('Education'), blank=True)

    experience = models.TextField(_('Experience'), blank=True)

    profile_pic = models.ImageField(_('Profile Picture'),
                                    upload_to='photos/',
                                    blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class User(AbstractUser, BaseProfileModel):

    remarks = models.TextField(_('Comment'), blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
