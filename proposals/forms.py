from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Employee, Patent, Agent, ContactPerson, Client
from .widgets import AjaxSelect2MultipleWidget, AjaxSelect2Widget, MySelect2Widget


class ContactPersonModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactPersonModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = ContactPerson
        fields = ('name', 'title', 'ext_number', 'email', 'remarks')


class AjaxContactPersonModelForm(ContactPersonModelForm):
    def __init__(self, *args, **kwargs):
        super(AjaxContactPersonModelForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse("proposals:contact_person-create")


class EmployeeModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Employee
        fields = ('chinese_name', 'english_name', 'id_number', 'gender', 'email', 'county', 'address',
                  'home_number', 'office_number', 'employee_id', 'engagement_date', 'title_id',
                  'spouse_name', 'education', 'experience', 'remarks')
        widgets = {
            "gender": MySelect2Widget(),
        }


class AgentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Agent
        fields = ('agent_title', 'country', 'representative', 'email', 'contact_person',
                  'office_number', 'remarks')
        widgets = {
            'contact_person': AjaxSelect2Widget(search_fields=["name__icontains"]),
        }


class AjaxAgentModelForm(AgentModelForm):
    def __init__(self, *args, **kwargs):
        super(AjaxAgentModelForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse("proposals:agent-create")

    class Meta(AgentModelForm.Meta):
        widgets = {
            'contact_person': MySelect2Widget(),
        }


class ClientModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Client
        fields = ('abbr_client', 'client_ch_name', 'client_en_name', 'country',
                  'post_address', 'english_address', 'invoice_address', 'phone_number',
                  'fax_number', 'contact_person1', 'contact_person2', 'repr_chinese_name',
                  'repr_english_name', 'vat_no', 'number_employee', 'primary_owner',
                  'secondary_owner', 'status', 'remarks')

        widgets = {
            'contact_person1': AjaxSelect2Widget(search_fields=["name__icontains"],
                                                 able_ajax_create=True,
                                                 modelform=ContactPersonModelForm),
            'contact_person2': AjaxSelect2Widget(search_fields=["name__icontains"],
                                                 able_ajax_create=True,
                                                 modelform=ContactPersonModelForm),
        }


class AjaxClientModelForm(ClientModelForm):
    def __init__(self, *args, **kwargs):
        super(AjaxClientModelForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse("proposals:client-create")

    class Meta(ClientModelForm.Meta):
        widgets = {
            'contact_person1': AjaxSelect2Widget(search_fields=["name__icontains"]),
            'contact_person2': AjaxSelect2Widget(search_fields=["name__icontains"]),
        }


class PatentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatentModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))


    class Meta:
        model = Patent
        fields = ('case_id', 'chinese_title', 'english_title', 'client', 'client_type',
                  'client_ref_no', 'country', 'request_examination', 'examination_date',
                  'inventor', 'case_status', 'filing_date', 'application_no', 'publication_date',
                  'publication_no', 'patent_date', 'patent_no', 'patent_term', 'certificate_no',
                  'local_agent', 'foreign_agent', 'pre_decision_date', 'pre_decision_no',
                  're_examine_date', 'control_item', 'control_date', 'deadline', 'description_pages',
                  'drawing_pages', 'figures_number', 'owner', 'priority', 'prio_country', 'prio_application_no',
                  'prio_filing_date', 'file_holder_position', 'IDS_infomation', 'remarks')

        widgets = {
            'client': AjaxSelect2Widget(search_fields=["client_en_name__icontains", "client_ch_name__icontains"],
                                        able_ajax_create=True,
                                        modelform=AjaxClientModelForm),
            'local_agent': AjaxSelect2Widget(search_fields=["agent_title__icontains"],
                                             able_ajax_create=True,
                                             modelform=AjaxAgentModelForm),
            'foreign_agent': AjaxSelect2Widget(search_fields=["agent_title__icontains", ],
                                               able_ajax_create=True,
                                               modelform=AjaxAgentModelForm),
            'inventor': AjaxSelect2MultipleWidget(search_fields=['chinese_name__icontains', 'english_name__icontains']),
            'client_type': MySelect2Widget(),
            'country': MySelect2Widget(),
            'request_examination': MySelect2Widget(),
            'case_status': MySelect2Widget(),
            'control_item': MySelect2Widget(),
            'priority': MySelect2Widget(),
            'prio_country': MySelect2Widget(),
        }
