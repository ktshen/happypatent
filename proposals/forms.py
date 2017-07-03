from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder

from .models import Employee, Patent, Agent, Client, Inventor, ControlEvent
from .widgets import AjaxSelect2Widget, AjaxSelect2MultipleWidget, MySelect2Widget
from .utils import file_validate, YES_OR_NO


class EmployeeModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    'chinese_name',
                    'english_name',
                    css_class="form_wrap"
                ),
                Div(
                    'id_number',
                    'title_id',
                    css_class="form_wrap"
                ),
                Div(
                    'email',
                    'office_number',
                    css_class="form_wrap"
                ),
                Div(
                    'home_number',
                    'engagement_date',
                    css_class="form_wrap"
                ),
                Div(
                    'county',
                    'address',
                    css_class="form_wrap"
                ),
                Div(
                    'gender',
                    'spouse_name',
                    css_class="form_wrap"
                ),
                Div(
                    'education',
                    'experience',
                    css_class="form_wrap"
                ),
                Div(
                    Div(
                        'remarks',
                        css_class="form_wrap"
                    ),
                    ButtonHolder(Submit('save', 'save')),
                    css_class="remark_wrap"
                )

            )
        )

    class Meta:
        model = Employee
        fields = ('chinese_name', 'english_name', 'id_number', 'gender', 'email', 'county', 'address',
                  'home_number', 'office_number', 'engagement_date', 'title_id',
                  'spouse_name', 'education', 'experience', 'remarks')
        widgets = {
            "gender": MySelect2Widget(),
            "title_id": MySelect2Widget(),
        }


class InventorModelForm(forms.ModelForm):
    client_id = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"type": "hidden"}))

    def __init__(self, *args, **kwargs):
        super(InventorModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Inventor
        fields = ('chinese_name', 'english_name', 'country', 'post_address',
                  'english_address', 'phone_number', 'id_number', 'email', 'remarks')


class AgentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Div(
                        'agent_title',
                        'contact_person_name',
                        css_class="form_wrap"
                    ),
                    Div(
                        'contact_person_phone_number',
                        'contact_person_email',
                        css_class="form_wrap"
                    ),
                    Div(
                        'country',
                        'address',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'beneficiary_name',
                        'beneficiary_no',
                        css_class="form_wrap"
                    ),
                    Div(
                        'remittance_bank',
                        css_class="form_wrap"
                    ),
                    css_class="related",
                ),
                Div(
                    Div(
                        'remarks',
                        css_class="form_wrap"
                    ),
                    ButtonHolder(Submit('save', 'save')),
                    css_class="remark_wrap"
                )
            )
        )

    class Meta:
        model = Agent
        fields = ('agent_title', 'country', 'address', 'contact_person_name', 'contact_person_phone_number',
                  'contact_person_email', 'beneficiary_name', 'remittance_bank', 'beneficiary_no', 'remarks')

    class Media:
        js = []
        css = {
            'all': ('css/agent_create.css',)
        }


class ClientModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Div(
                        'client_ch_name',
                        'client_en_name',
                        css_class="form_wrap"
                    ),
                    Div(
                        'abbr_client',
                        'country',
                        css_class="form_wrap"

                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'post_address',
                        'english_address',
                        css_class="form_wrap"
                    ),
                    Div(
                        'invoice_address',
                        'phone_number',
                        css_class="form_wrap"
                    ),
                    Div(

                        'fax_number',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'repr_chinese_name',
                        'repr_english_name',
                        css_class="form_wrap"
                    ),
                    Div(
                        'contact_person_name',
                        'contact_person_title',
                        css_class="form_wrap"
                    ),
                    Div(
                        'contact_person_phone_number',
                        'contact_person_email',
                        css_class="form_wrap"
                    ),
                    Div(
                        'primary_owner',
                        'secondary_owner',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'vat_no',
                        'number_employee',

                        css_class="form_wrap"
                    ),
                    Div(
                        'status',
                        css_class="form_wrap",
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'remarks',
                        css_class="form_wrap"
                    ),
                    ButtonHolder(Submit('save', 'save')),
                    css_class="remark_wrap"
                )
            )
        )

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
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Div(
                        'case_id',
                        'case_status',
                        css_class="form_wrap"
                    ),
                    Div(
                        'english_title',
                        'chinese_title',
                        css_class="form_wrap"
                    ),
                    Div(
                        'patent_date',
                        'patent_no',
                        css_class="form_wrap"
                    ),
                    Div(
                        'patent_term',
                        'certificate_no',
                        css_class="form_wrap"
                    ),
                    Div(
                        'inventor',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'client',
                        'client_ref_no',
                        css_class="form_wrap"
                    ),
                    Div(
                        'agent',
                        'agent_ref_no',
                        css_class="form_wrap"
                    ),
                    Div(
                        'deadline',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'priority',
                        'prio_country',
                        css_class="form_wrap"
                    ),
                    Div(
                        'prio_application_no',
                        'prio_filing_date',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'application_type',
                        'country',
                        css_class="form_wrap"
                    ),
                    Div(
                        'application_no',
                        'filing_date',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'request_examination',
                        'examination_date',
                        css_class="form_wrap"
                    ),
                    Div(
                        're_examine_date',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'publication_date',
                        'publication_no',
                        css_class="form_wrap"
                    ),
                    Div(
                        'pre_decision_date',
                        'pre_decision_no',
                        css_class="form_wrap"
                    ),

                    Div(
                        'control_item',
                        'control_date',

                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'description_pages',
                        'drawing_pages',
                        css_class="form_wrap"
                    ),
                    Div(
                        'figures_number',
                        'owner',
                        css_class="form_wrap"
                    ),

                    Div(
                        'file_holder_position',
                        'IDS_information',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'remarks',
                        css_class="form_wrap"
                    ),
                    ButtonHolder(Submit('save', 'save')),
                    css_class="remark_wrap"
                ),
                'file'
            )
        )

    class Meta:
        model = Patent
        fields = ('case_id', 'chinese_title', 'english_title', 'client', 'client_ref_no',
                  'application_type', 'country', 'request_examination', 'examination_date',
                  'inventor', 'case_status', 'filing_date', 'extended_days', 'patent_term', 'application_no',
                  'publication_date', 'publication_no', 'patent_date', 'patent_no', 'certificate_no',
                  'agent', 'agent_ref_no', 'pre_decision_date', 'pre_decision_no',
                  're_examine_date', 'description_pages', 'drawing_pages', 'figures_number', 'priority',
                  'prio_country', 'prio_application_no', 'prio_filing_date', 'file_holder_position',
                  'IDS_information', 'remarks', 'file')

        widgets = {
            'client': AjaxSelect2Widget("proposals:client-select2",
                                        create_new=True,
                                        create_new_url="proposals:client-create"),
            'agent': AjaxSelect2Widget("proposals:agent-select2",
                                       create_new=True,
                                       create_new_url="proposals:agent-create"),
            'inventor': AjaxSelect2MultipleWidget("proposals:inventor-select2"),
            'application_type': MySelect2Widget(),
            'number_employee': MySelect2Widget(),
            'country': MySelect2Widget(),
            'request_examination': MySelect2Widget(),
            'case_status': MySelect2Widget(),
            'priority': MySelect2Widget(),
            'prio_country': MySelect2Widget(),
            'patent_term_activation': MySelect2Widget(),
        }


class ControlEventModelForm(forms.ModelForm):
    case_id = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"type": "hidden"}))

    def __init__(self, *args, **kwargs):
        super(ControlEventModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Div(
                        'chinese_name',
                        'english_name',
                        css_class="form_wrap"
                    ),
                    Div(
                        'id_number',

                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'client',
                        'country',
                        css_class="form_wrap"
                    ),

                    Div(
                        'post_address',
                        'english_address',
                        css_class="form_wrap"
                    ),
                    Div(
                        'phone_number',
                        'email',
                        css_class="form_wrap"
                    ),
                    css_class="related"
                ),
                Div(
                    Div(
                        'remarks',
                        css_class="form_wrap"
                    ),
                    ButtonHolder(Submit('save', 'save')),
                    css_class="remark_wrap"
                )

            )
        )

    class Meta:
        model = ControlEvent
        fields = ('control_item', 'control_date', 'deadline', "complete_date", "remarks")
        widgets = {
            'control_item': MySelect2Widget(),
        }
