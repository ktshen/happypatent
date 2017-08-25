from __future__ import unicode_literals
from django.db import models
from django.urls.base import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from happypatent.users.models import BaseProfileModel, User
from happypatent.base.models import BaseModel
from fileattachments.models import FileAttachment


YES_OR_NO = (
    ('yes', 'Yes'),
    ('no', 'No')
)


@python_2_unicode_compatible
class Inventor(BaseModel):
    chinese_name = models.CharField(_('Chinese name'), max_length=50)
    english_name = models.CharField(_('English name (Last Name, First Name)'), max_length=50)
    country = models.CharField(_('Country'), max_length=50)
    post_address = models.CharField(_('Post Office Address'), max_length=100)
    english_address = models.CharField(_('English Address'), max_length=100)
    phone_number = models.CharField(_('Phone Number'), max_length=50, blank=True)
    id_number = models.CharField(_('ID Number'), max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.chinese_name

    def get_absolute_url(self):
        return reverse("proposals:inventor-detail", args=[self.pk])


@python_2_unicode_compatible
class Proposal(BaseModel):
    APPRAISAL_RESULT_CHOICES = (
        ('pass', _('Pass')),
        ('fail', _('Fail')),
        ('re-appraise', _('Re-appraise after supplements')),
    )
    proposal_id = models.CharField(_('Proposal ID'), max_length=50, blank=True)
    chinese_title = models.CharField(_('Chinese Title'), max_length=200)
    english_title = models.CharField(_('English Title'), max_length=200)
    inventors = models.ManyToManyField(verbose_name=_('Inventor'), to=Inventor)
    department = models.CharField(_('Department'), blank=True, max_length=200)
    category = models.CharField(_('Technique category'), blank=True, max_length=200)
    proposal_date = models.DateField(_('Proposal Date'), blank=True, null=True)
    country = models.CharField(_('Default Filing Countries'), blank=True, max_length=200)
    abstract = models.TextField(_('Abstract'), blank=True)
    performance = models.CharField(_('Applied field and performance'), blank=True, max_length=200)
    appraisal_date = models.DateField(_('Appraisal date'), blank=True, null=True)
    appraisal_result = models.CharField(_('Appraisal Results'), choices=APPRAISAL_RESULT_CHOICES, blank=True,
                                        max_length=200)
    files = GenericRelation(FileAttachment, related_query_name='proposal')

    def __str__(self):
        return self.chinese_title

    def get_absolute_url(self):
        return reverse("proposals:proposal-detail", args=[self.pk])

    def appraisal_result_template(self):
        if self.appraisal_result:
            return dict(Proposal.APPRAISAL_RESULT_CHOICES)[self.appraisal_result]
        else:
            return self.appraisal_result


@python_2_unicode_compatible
class Agent(BaseModel):
    agent_id = models.AutoField(_('Agent\'s ID'), primary_key=True, editable=False)
    agent_title = models.CharField(_('Agent\'s title'), max_length=50, unique=True)
    country = models.CharField(_('Country'), max_length=50)
    address = models.CharField(_("Address"), max_length=100, blank=True)
    beneficiary_name = models.CharField(_("Beneficiary Name"), max_length=50, blank=True)
    remittance_bank = models.CharField(_("Remittance Bank"), max_length=50, blank=True)
    beneficiary_no = models.CharField(_("Beneficiary A/C No."), max_length=50, blank=True)
    contact_person_name = models.CharField(_('Contact Person\'s Name'), max_length=30, blank=True)
    contact_person_phone_number = models.CharField(_('Contact Person\'s Phone Number'), max_length=50, blank=True)
    contact_person_email = models.EmailField(_('Contact Person\'s Email'), blank=True)

    def __str__(self):
        return str(self.agent_title)

    def get_absolute_url(self):
        return reverse("proposals:agent-detail", args=[self.agent_id])

    @property
    def pk(self):
        return self.agent_id


@python_2_unicode_compatible
class Patent(BaseModel):
    APPLICATION_TYPE_CHOICES = (
        ('invention', _('Invention')),
        ('utility', _('Utility')),
        ('design', _('Design')),
        ('trademark', _('Trademark')),
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
        ('12', _('Allowed')),
        ('13', _('Abandoned')),
        ('14', _('Invalidation examination')),
    )

    case_id = models.CharField(_('Case ID'), max_length=30, unique=True)
    chinese_title = models.CharField(_('Chinese Title'), max_length=100)
    english_title = models.CharField(_('English Title'), max_length=100)
    application_type = models.CharField(_('Type'), max_length=30,
                                        choices=APPLICATION_TYPE_CHOICES, blank=True)
    country = models.CharField(_('Country'), max_length=30,
                               choices=COUNTRY_CHOICES)
    inventor = models.ManyToManyField(verbose_name=_('Inventor'), to=Inventor, blank=True)

    case_status = models.CharField(_('Status'), max_length=30,
                                   choices=CASE_STATUS_CHOICES, blank=True)

    agent = models.ForeignKey(verbose_name=_("Agent"), to=Agent, related_name='patent_agent',
                              on_delete=models.SET_NULL, null=True, blank=True)
    agent_ref_no = models.CharField(_("Agent Ref. No."), max_length=15, blank=True)

    application_no = models.CharField(_('Application No.'), max_length=30, blank=True)
    filing_date = models.DateField(_('Filing Date'), blank=True, null=True)
    extended_days = models.PositiveIntegerField("Extended Days (days)", blank=True, default=0)
    publication_date = models.DateField(_('Publication Date'), blank=True, null=True)
    publication_no = models.CharField(_('Publication No.'), max_length=30, blank=True)
    patent_date = models.DateField(_('Date of patent'), blank=True, null=True)
    patent_no = models.CharField(_('Patent No.'), max_length=30, blank=True)

    pre_decision_date = models.DateField(_('Date of preliminary decision'), blank=True, null=True)
    pre_decision_no = models.CharField(_('Preliminary decision No.'), max_length=30, blank=True)
    re_examine_date = models.DateField(_('Date of re-examination'), blank=True, null=True)

    description_pages = models.PositiveIntegerField(_('Number of description pages'), blank=True, null=True)
    drawing_pages = models.PositiveIntegerField(_('Number of drawing pages'), blank=True, null=True)
    figures_number = models.PositiveIntegerField(_('Number of figures'), blank=True, null=True)

    request_examination = models.CharField(_('Request Examination'), max_length=30,
                                           choices=YES_OR_NO, blank=True)
    examination_date = models.DateField(_('Date of request examination'), blank=True, null=True)
    patent_term = models.DateField(_('Patent Term.'), blank=True, null=True)
    final_patent_term = models.DateField(_('Final Patent Term.'), blank=True, null=True)

    certificate_no = models.CharField(_('Certificate No.'), max_length=30, blank=True)

    priority = models.CharField(_('Priority'), max_length=30, choices=YES_OR_NO, default='no')
    prio_country = models.CharField(_('(Priority) Country'), max_length=30,
                                    choices=COUNTRY_CHOICES, blank=True)
    prio_application_no = models.CharField(_('(Priority) Application No.'), max_length=30, blank=True)
    prio_filing_date = models.DateField(_('(Priority) Filing Date'), blank=True, null=True)

    file_holder_position = models.CharField(_("File-holder position"), max_length=100, blank=True)
    IDS_information = models.TextField(_('IDS Information'), blank=True)
    files = GenericRelation(FileAttachment, related_query_name='patent')

    def __str__(self):
        return self.case_id

    def get_absolute_url(self):
        return reverse("proposals:patent-detail", args=[self.case_id])

    def case_status_template(self):
        if self.case_status:
            return dict(Patent.CASE_STATUS_CHOICES)[self.case_status]
        else:
            return self.case_status

    def application_type_template(self):
        if self.application_type:
            return dict(Patent.APPLICATION_TYPE_CHOICES)[self.application_type]
        else:
            return self.application_type

    def country_template(self):
        if self.country:
            return str(dict(Patent.COUNTRY_CHOICES)[self.country])
        else:
            return self.country


@python_2_unicode_compatible
class ControlEvent(BaseModel):
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
    control_item = models.CharField(_('Control Item'), max_length=30,
                                    choices=CONTROL_ITEM_CHOICES)
    control_date = models.DateField(_('Control Date'))
    deadline = models.DateField(_('Deadline'))
    complete_date = models.DateField(_("Complete Date"), null=True, blank=True)
    patent = models.ForeignKey(to=Patent, on_delete=models.CASCADE, related_name="control_event", null=True)

    def __str__(self):
        return "ControlEvent_" + str(self.patent) + "_" + self.control_item_verbal(self.control_item)

    def control_item_template(self):
        if self.control_item:
            return self.control_item_verbal(self.control_item)
        else:
            return self.control_item

    @staticmethod
    def control_item_verbal(control_item):
        return str(dict(ControlEvent.CONTROL_ITEM_CHOICES)[control_item])

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"


@python_2_unicode_compatible
class Work(BaseModel):
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
