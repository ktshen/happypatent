from __future__ import unicode_literals
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from happypatent.users.models import BaseProfileModel, User


@python_2_unicode_compatible
class _BaseModel(models.Model):
    remarks = models.TextField(_('Remarks'), blank=True)

    created_by = models.ForeignKey(verbose_name=_("Created by"),
                                   to=User,
                                   on_delete=models.SET_NULL,
                                   null=True)

    created = models.DateTimeField(_('Created Time'),
                                   auto_now=True)

    update = models.DateTimeField(_('Latest Update'),
                                  auto_now_add=True,
                                  null=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Employee(BaseProfileModel, _BaseModel):
    GENDER_CHOICE = (
        ('m', _('Male')),
        ('f', _('Female'))
    )
    chinese_name = models.CharField(_("Chinese Name"),
                                    max_length=30,
                                    blank=True)

    english_name = models.CharField(_('English Name'),
                                    max_length=30,
                                    blank=True)

    employee_id = models.CharField(_('Employee ID'),
                                   max_length=20,
                                   unique=True)

    email = models.EmailField()

    engagement_date = models.DateField(_('Engagement Date'),
                                       default=timezone.now)

    title_id = models.CharField(_('Title Id'),
                                max_length=30,
                                blank=True)

    def __str__(self):
        return self.employee_id

    def get_absolute_url(self):
        return reverse("proposals:employee-detail", args=[self.pk, ])


@python_2_unicode_compatible
class ContactPerson(_BaseModel):
    name = models.CharField(_('Name'), max_length=30, default=" ")
    title = models.CharField(_('Title'), max_length=30, blank=True)
    ext_number = models.CharField(_('Ext.'), max_length=50)
    email = models.EmailField(_('Email'))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Client(_BaseModel):
    client_id = models.AutoField(_('Client ID'), primary_key=True, editable=False)
    abbr_client = models.CharField(_('Client name in abbreviated form'), max_length=30)
    client_ch_name = models.CharField(_('Client Chinese name'), max_length=50)
    client_en_name = models.CharField(_('Client English name'), max_length=50)
    country = models.CharField(_('Country'), max_length=50)
    post_address = models.CharField(_('Post Office Address'), max_length=100)
    english_address = models.CharField(_('English Address'), max_length=100, blank=True)
    invoice_address = models.CharField(_('Invoice(Application form) address'), max_length=100, blank=True)
    phone_number = models.CharField(_('Phone Number'), max_length=50)
    fax_number = models.CharField(_('Fax Number'), max_length=50, blank=True)
    contact_person1 = models.ForeignKey(to=ContactPerson, on_delete=models.CASCADE, related_name="client1",
                                        null=True)
    contact_person2 = models.ForeignKey(to=ContactPerson, on_delete=models.SET_NULL, null=True,
                                        related_name="client2", blank=True)
    repr_chinese_name = models.CharField(_('Representative\'s Chinese name'), max_length=50)
    repr_english_name = models.CharField(_('Representative\'s English name'), max_length=50)
    vat_no = models.CharField(_('VAT No.'), max_length=30)
    number_employee = models.IntegerField(_('Number of employees'))
    primary_owner = models.CharField(_('Primary owner'), max_length=50)
    secondary_owner = models.CharField(_('Secondary owner'), max_length=50, blank=True)
    status = models.CharField(_('Status'), max_length=30, blank=True)

    class Meta:
        verbose_name = _('Applicant')
        verbose_name_plural = _('Applicants')

    def __str__(self):
        return self.name

    @property
    def name(self):
        """
        Get both Chinese and English name
        """
        return self.client_ch_name

    def get_absolute_url(self):
        return reverse("proposals:client-detail", args=[self.client_id])

    @property
    def pk(self):
        return self.client_id


@python_2_unicode_compatible
class Agent(_BaseModel):
    agent_id = models.AutoField(_('Client ID'), primary_key=True, editable=False)
    agent_title = models.CharField(_('Agent\'s title'), max_length=50, unique=True)
    country = models.CharField(_('Country'), max_length=50)
    representative = models.CharField(_('Representative'), max_length=50)
    email = models.EmailField(blank=True)
    contact_person = models.ForeignKey(to=ContactPerson, on_delete=models.SET_NULL, null=True, blank=True)
    office_number = models.CharField(_('Office Number(ext. personal)'), max_length=50)

    def __str__(self):
        return str(self.agent_title)

    def get_absolute_url(self):
        return reverse("proposals:agent-detail", args=[self.agent_id])

    @property
    def pk(self):
        return self.agent_id


@python_2_unicode_compatible
class Patent(_BaseModel):
    APPLICATION_TYPE_CHOICES = (
        ('invention', _('Invention')),
        ('utility', _('Utility')),
        ('design', _('Design')),
    )
    COUNTRY_CHOICES = (
        ('TW', 'TW'),
        ('US', 'US'),
        ('CN', 'CN'),
        ('JP', 'JP'),
        ('KR', 'KR'),
        ('EP', 'EP'),
        ('GB', 'GB'),
        ('DE', 'DE'),
        ('FR', 'FR'),
    )
    YES_OR_NO = (
        ('yes', 'Yes'),
        ('no', 'No')
    )
    CASE_STATUS_CHOICES = (
        ('1', _('Draft/Translation')),
        ('2', _('Preliminary examination')),
        ('3', _('Response/Amendment-1')),
        ('4', _('Response/amendment-2')),
        ('5', _('Rejection')),
        ('6', _('Publication')),
        ('7', _('Re-examination')),
        ('8', _('Appeal')),
        ('9', _('Re-appeal')),
        ('10', _('Administrative litigation')),
        ('11', _('Paying issue fee')),
        ('12', _('Patent allowed')),
        ('13', _('Client abandon')),
        ('14', _('Invalidation examination')),
    )
    CONTROL_ITEM_CHOICES = (
        ('1', _('File new application')),
        ('2', _('File Chinese description')),
        ('3', _('Request examination')),
        ('4', _('File patent invalidation')),
        ('5', _('File re-examination')),
        ('6', _('File amendment')),
        ('7', _('File response')),
        ('8', _('Pay issue fee')),
        ('9', _('Pay maintenance fee')),
        ('10', _('Pay annuity fee')),
        ('11', _('File appeal')),
        ('12', _('File re-appeal')),
        ('13', _('File administrative litigation')),
        ('14', _('Other')),
    )

    case_id = models.CharField(_('Case ID'), max_length=30, unique=True)
    # our_ref_no = pk
    chinese_title = models.CharField(_('Chinese Title'), max_length=100)
    english_title = models.CharField(_('English Title'), max_length=100)
    client = models.ForeignKey(to=Client, on_delete=models.SET_NULL, null=True)
    client_type = models.CharField(_('Type'), max_length=30,
                                   choices=APPLICATION_TYPE_CHOICES, blank=True)
    client_ref_no = models.CharField(_('Client\'s ref. No.'), max_length=30)
    country = models.CharField(_('Country'), max_length=30,
                               choices=COUNTRY_CHOICES)
    request_examination = models.CharField(_('Request Examination'), max_length=30,
                                           choices=YES_OR_NO, blank=True)
    examination_date = models.DateField(_('Date of request examination'), blank=True, null=True)
    inventor = models.ManyToManyField(verbose_name=_('Inventor'), to=Employee)
    case_status = models.CharField(_('Status'), max_length=30,
                                   choices=CASE_STATUS_CHOICES, default='1')
    filing_date = models.DateField(_('Filing Date'), blank=True, null=True)
    application_no = models.CharField(_('Application No.'), max_length=30, blank=True)
    publication_date = models.DateField(_('Publication Date'), blank=True, null=True)
    publication_no = models.CharField(_('Publication No.'), max_length=30, blank=True)
    patent_date = models.DateField(_('Date of patent'), blank=True, null=True)
    patent_no = models.CharField(_('Patent No.'), max_length=30, blank=True)
    patent_term = models.DateField(_('Patent Term.'), blank=True, null=True)
    certificate_no = models.CharField(_('Certificate No.'), max_length=30, blank=True)

    local_agent = models.ForeignKey(to=Agent, related_name='patent_local_agent',
                                    on_delete=models.SET_NULL, null=True)
    foreign_agent = models.ForeignKey(to=Agent, related_name='patent_foreign_agent',
                                      on_delete=models.SET_NULL, null=True)
    pre_decision_date = models.DateField(_('Date of preliminary decision'), blank=True, null=True)
    pre_decision_no = models.CharField(_('Preliminary decision No.'), max_length=30, blank=True)
    re_examine_date = models.DateField(_('Date of re-examination'), blank=True, null=True)

    control_item = models.CharField(_('Control Item'), max_length=30,
                                    choices=CONTROL_ITEM_CHOICES, default='1')
    control_date = models.DateField(_('Control Date'), null=True)
    deadline = models.DateField(_('Deadline'), null=True)

    description_pages = models.IntegerField(_('Number of description pages'), blank=True, null=True)
    drawing_pages = models.IntegerField(_('Number of drawing pages'), blank=True, null=True)
    figures_number = models.IntegerField(_('Number of figures'), blank=True, null=True)
    owner = models.CharField(_('Owner'), max_length=50)

    priority = models.CharField(_('Priority'), max_length=30, choices=YES_OR_NO, default='no')
    prio_country = models.CharField(_('(Priority) Country'), max_length=30,
                                    choices=COUNTRY_CHOICES, blank=True)
    prio_application_no = models.CharField(_('(Priority) Application No.'), max_length=30, blank=True)
    prio_filing_date = models.DateField(_('(Priority) Filing Date'), blank=True, null=True)

    file_holder_position = models.CharField(_("File-holder position"), max_length=100, blank=True)
    IDS_infomation = models.CharField(_('IDS Information'), max_length=100, blank=True)

    def __str__(self):
        return self.case_id

    def get_absolute_url(self):
        pass


@python_2_unicode_compatible
class Work(_BaseModel):
    WORK_TYPE_ID_CHOICES = (
        ('1', _('File new application')),
        ('2', _('File document')),
        ('3', _('Request examination')),
        ('4', _('File patent invalidation')),
        ('5', _('File re-examination')),
        ('6', _('File amendment')),
        ('7', _('File response')),
        ('8', _('Pay issue fee')),
        ('9', _('Pay maintenance fee')),
        ('10', _('Pay annuity fee')),
        ('11', _('File appeal')),
        ('12', _('File re-appeal')),
        ('13', _('File administrative litigation')),
        ('14', _('Other')),
    )
    work_id = models.CharField(_('Work ID'), max_length=30, unique=True)
    case_id = models.CharField(_('Case ID'), max_length=30)
    person_charge = models.CharField(_('Person in charge'), max_length=50)
    work_type_id = models.CharField(_('Work Type ID'), max_length=50,
                                    choices=WORK_TYPE_ID_CHOICES, default='1')
    work_stage_id = models.CharField(_('Work Stage ID'), max_length=30)
    control_deadline = models.DateField(_('Control Deadline'))
    distribution_deadline = models.DateField(_('Distribution Deadline'), blank=True, null=True)
    control_person = models.CharField(_('Control Person'), max_length=50, blank=True)
    distributor = models.CharField(_('Distributor'), max_length=50, blank=True)
    status = models.CharField(_('Status'), max_length=50, blank=True)
    closed_case = models.BooleanField(verbose_name=('Closed Case'), default=False)

    def __str__(self):
        return self.work_id


class Test1(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("proposals:test1-detail", args=[self.pk, ])


class Test2(models.Model):
    name = models.CharField(max_length=50)
    m2m = models.ManyToManyField(to=Test1)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse("proposals:test-detail", args=[self.pk, ])

    def __str__(self):
        return self.name
