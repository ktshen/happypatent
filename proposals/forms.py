from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Div,Fieldset

from .models import Employee, Patent, Agent, Client, Inventor
from .widgets import AjaxSelect2MultipleWidget, AjaxSelect2Widget, MySelect2Widget
from .utils import file_validate


class EmployeeModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Employee
        fields = ('chinese_name', 'english_name', 'id_number', 'gender', 'email', 'county', 'address',
                  'home_number', 'office_number', 'engagement_date', 'title_id',
                  'spouse_name', 'education', 'experience', 'remarks')
        widgets = {
            "gender": MySelect2Widget(),
            "title_id": MySelect2Widget(),
        }


class AgentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout=Layout(
            Fieldset(
                "",
                Div(

                   'agent_title',
                    'country',


                    style="display:flex;flex-direction:row",
                    css_class="form-wrap"
                ),
                Div(

                    'address',
                    'contact_person_name',

                    style="display:flex;flex-direction:row",
                    css_class="form-wrap"
                ),
                Div(

                    'contact_person_phone_number',
                    'contact_person_email',
                    style="display:flex;flex-direction:row",
                    css_class="form-wrap"

                ),


                Div(

                    'beneficiary_name',
                    'remittance_bank',
                    style="display:flex;flex-direction:row",
                    css_class="form-wrap"
                ),
                Div(

                    'beneficiary_no',
                    style="display:flex;flex-direction:row",
                    css_class="form-wrap"
                ),
                Div(
                    'remarks',
                    css_class="except"
                )
            )
        )
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Agent
        fields = ('agent_title', 'country', 'address', 'contact_person_name', 'contact_person_phone_number',
                  'contact_person_email', 'beneficiary_name', 'remittance_bank', 'beneficiary_no', 'remarks')

    class Media:
        js = []
        css = {
            'all': ('css/agent_create.css',)
        }


class AjaxAgentModelForm(AgentModelForm):
    def __init__(self, *args, **kwargs):
        super(AjaxAgentModelForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse("proposals:agent-create")


class ClientModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Client
        fields = ('abbr_client', 'client_ch_name', 'client_en_name', 'country',
                  'post_address', 'english_address', 'invoice_address', 'phone_number',
                  'fax_number', 'contact_person_name', 'contact_person_title',
                  'contact_person_phone_number', 'contact_person_email', 'repr_chinese_name',
                  'repr_english_name', 'vat_no', 'number_employee', 'primary_owner',
                  'secondary_owner', 'status', 'remarks')
        widgets = {
            "number_employee": MySelect2Widget(),
        }


class AjaxClientModelForm(ClientModelForm):
    def __init__(self, *args, **kwargs):
        super(AjaxClientModelForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse("proposals:client-create")


class PatentModelForm(forms.ModelForm):
    file = forms.FileField(label="Files",
                           widget=forms.ClearableFileInput(attrs={'multiple': True}),
                           validators=[file_validate],
                           required=False)

    def __init__(self, *args, **kwargs):
        super(PatentModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Submit'))

    class Meta:
        model = Patent
        fields = ('case_id', 'chinese_title', 'english_title', 'client', 'application_type',
                  'country', 'request_examination', 'examination_date',
                  'inventor', 'case_status', 'filing_date', 'application_no', 'publication_date',
                  'publication_no', 'patent_date', 'patent_no', 'patent_term', 'certificate_no',
                  'local_agent', 'foreign_agent', 'pre_decision_date', 'pre_decision_no',
                  're_examine_date', 'control_item', 'control_date', 'deadline', 'description_pages',
                  'drawing_pages', 'figures_number', 'owner', 'priority', 'prio_country', 'prio_application_no',
                  'prio_filing_date', 'file_holder_position', 'IDS_infomation', 'remarks', 'file')

        widgets = {
            # 'case_id': forms.TextInput(attrs={"readonly": True}),
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
            'application_type': MySelect2Widget(),
            'number_employee': MySelect2Widget(),
            'country': MySelect2Widget(),
            'request_examination': MySelect2Widget(),
            'case_status': MySelect2Widget(),
            'control_item': MySelect2Widget(),
            'priority': MySelect2Widget(),
            'prio_country': MySelect2Widget(),
        }


class InventorModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InventorModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Inventor
        fields = ('chinese_name', 'english_name', 'client', 'country', 'post_address',
                  'english_address', 'phone_number', 'id_number', 'email', 'remarks')

        widgets = {
            'client': MySelect2Widget(),
        }
