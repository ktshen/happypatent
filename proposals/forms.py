from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder
from .models import Patent, Agent, Proposal, Inventor, ControlEvent
from .widgets import AjaxSelect2Widget, AjaxSelect2MultipleWidget, MySelect2Widget


class InventorModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InventorModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Div(

                        'chinese_name',
                        'phone_number',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'english_name',
                        'id_number',

                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'country',
                        'department',
                        css_class="col-md-4 col-sm-6"
                    ),
                    css_class="row green-border"
                ),
                Div(
                    Div(
                        'post_address',
                        'english_address',
                        'email',
                        css_class="col-md-8 col-sm-8"
                    ),
                    css_class="row grey-border"
                ),
                Div(
                    Div(
                        'remarks',
                        css_class="col-md-8 col-sm-8"
                    ),
                    css_class="row green-border"
                ),
                Div(
                    Div(
                        ButtonHolder(Submit('save', 'save',css_class='btn btn-primary')),
                        css_class="col-md-1 pull-right"
                    ),
                    css_class="row"
                )
            )
        )

    class Meta:
        model = Inventor
        fields = ('chinese_name', 'english_name', 'country', 'post_address', 'department',
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
                        'contact_person_phone_number',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'country',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'contact_person_name',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'contact_person_email',

                        css_class="col-md-8 col-sm-8"
                    ),
                    Div(
                        'address',
                        css_class="col-md-8"
                    ),
                    css_class="row green-border"
                ),
                Div(
                    Div(
                        'beneficiary_name',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'remittance_bank',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'beneficiary_no',
                        css_class="col-md-4 col-sm-6"
                    ),
                    css_class="row grey-border"
                ),
                Div(
                    Div(
                        'remarks',
                        css_class="col-md-8 col-sm-8"
                    ),
                    css_class="row green-border"
                ),
                Div(
                    ButtonHolder(Submit('save', 'save', css_class='btn btn-primary')),
                    css_class="col-md-1 pull-right"
                ),
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


class ProposalModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProposalModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout=Layout(
            Fieldset(
                "",
                Div(
                    Div(
                        'proposal_no',
                        'inventors',
                        'proposal_date',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'chinese_title',
                        'country',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'english_title',
                        'department',
                        css_class="col-md-4 col-sm-6"
                    ),
                    css_class="row green-border",
                ),
                Div(
                    Div(
                        'category',
                        'appraisal_result',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'performance',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'appraisal_date',
                        css_class="col-md-4 col-sm-6"
                    ),
                    css_class="row grey-border"
                ),
                Div(
                    Div(
                        'abstract',
                        css_class="col-md-6 col-sm-8"
                    ),
                    Div(
                        'remarks',
                        css_class="col-md-6 col-sm-8"
                    ),
                    css_class="row green-border"
                ),
                Div(
                    ButtonHolder(Submit('save', 'save', css_class='btn btn-primary')),
                    css_class="col-md-1 pull-right"
                ),
            )
        )

    class Meta:
        model = Proposal
        fields = ('chinese_title', 'english_title', 'inventors', 'department', 'category',
                  'proposal_date', 'country', 'abstract', 'performance', 'appraisal_date', 'appraisal_result',
                  'remarks')
        widgets = {
            'inventors': AjaxSelect2MultipleWidget("proposals:inventor-select2"),
            'appraisal_result': MySelect2Widget(),
        }


class PatentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatentModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Div(
                        'case_id',
                        'country',
                        css_class="col-md-4 col-sm-6 "
                    ),
                    Div(
                        'english_title',
                        'application_type',
                        css_class="col-md-4 col-sm-6 "
                    ),

                    Div(
                        'chinese_title',
                        'case_status',
                        css_class="col-md-4 col-sm-6"
                    ),
                    css_class="row  green-border"
                ),
                Div(
                    Div(
                        'inventor',
                        css_class="col-md-4 col-sm-6 "
                    ),
                    Div(
                        'agent_ref_no',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'agent',
                        css_class="col-md-4 col-sm-6 "
                    ),
                    css_class="row grey-border"
                ),
                Div(
                    Div(
                        'application_no',
                        'publication_date',
                        css_class="col-md-4 col-sm-6 "
                    ),
                    Div(
                        'request_examination',
                        'publication_no',
                         css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                       'examination_date',
                       'filing_date',
                        css_class="col-md-4 col-sm-6"
                    ),
                        css_class="row green-border"
                ),
                Div(
                    Div(
                        'pre_decision_date',
                        'description_pages',
                        css_class="col-md-4 col-sm-6 "
                    ),
                    Div(
                        'pre_decision_no',
                        'drawing_pages',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        're_examine_date',
                        'figures_number',
                        css_class="col-md-4 col-sm-6 "
                    ),
                    css_class="row grey-border"
                ),
                Div(
                    Div(
                        'patent_date',
                        'certificate_no',
                        css_class="col-md-4 col-sm-6"
                         ),
                    Div(
                        'patent_no',
                        'extended_days',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'patent_term',
                        css_class="col-md-4 col-sm-6"
                    ),
                      css_class="row  green-border"
                ),
                Div(
                    Div(
                        'priority',
                        'prio_filing_date',
                        css_class="col-md-4 col-sm-6 "
                    ),
                    Div(
                        'prio_country',
                        css_class="col-md-4 col-sm-6"
                    ),
                    Div(
                        'prio_application_no',
                        css_class="col-md-4 col-sm-6"
                    ),
                    css_class="row grey-border"
                ),
                Div(
                    Div(
                       'file_holder_position',
                        css_class="col-md-4 col-sm-6 "
                    ),
                    css_class="row green-border"
                ),
                Div(
                    Div(
                        'IDS_information',
                        css_class="col-md-6"
                    ),
                    Div(
                       'remarks',
                        css_class="col-md-6"
                        ),

                            css_class="row grey-border"
                ),
                Div(
                    ButtonHolder(Submit('save', 'save', css_class='btn btn-primary')),
                    css_class="col-md-1 pull-right"
                ),
            )
        )

    class Meta:
        model = Patent
        fields = ('case_id', 'chinese_title', 'english_title',
                  'application_type', 'country', 'request_examination', 'examination_date',
                  'inventor', 'case_status', 'filing_date', 'extended_days', 'patent_term', 'application_no',
                  'publication_date', 'publication_no', 'patent_date', 'patent_no', 'certificate_no',
                  'agent', 'agent_ref_no', 'pre_decision_date', 'pre_decision_no',
                  're_examine_date', 'description_pages', 'drawing_pages', 'figures_number', 'priority',
                  'prio_country', 'prio_application_no', 'prio_filing_date', 'file_holder_position',
                  'IDS_information', 'remarks')

        widgets = {
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
                Div('case_id'),
                Div(
                    Div(
                        'control_item',
                        'control_date',
                        css_class="column-wrap"
                    ),
                    Div(
                        'deadline',
                        'complete_date',
                        css_class="column-wrap"
                    ),
                    css_class="row"
                ),
                Div(
                    Div(
                        'remarks',
                        css_class="column-wrap"
                    ),
                    css_class="row"
                ),
                Div(
                    Div(
                        Div(
                            ButtonHolder(Submit('save', 'save',css_class='btn btn-primary ')),
                            css_class="button-wrap"
                        ),
                            css_class="row"
                    ),
                    css_class="row"
                ),
                Div(
                    ButtonHolder(Submit('save', 'save', css_class='btn btn-primary')),
                    css_class="col-md-1 pull-right"
                ),
            )
        )

    class Meta:
        model = ControlEvent
        fields = ('control_item', 'control_date', 'deadline', "complete_date", "remarks")
        widgets = {
            'control_item': MySelect2Widget(),
        }
