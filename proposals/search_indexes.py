from haystack import indexes
from .models import Patent, Agent, Inventor, Proposal


class PatentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    inventor = indexes.MultiValueField()
    agent = indexes.CharField(model_attr="agent", null=True)
    case_id = indexes.CharField(model_attr="case_id")
    chinese_title = indexes.CharField(model_attr="chinese_title")
    english_title = indexes.CharField(model_attr="english_title")
    agent_ref_no = indexes.CharField(model_attr="agent_ref_no")
    country = indexes.CharField(model_attr="country")
    application_no = indexes.CharField(model_attr="application_no")
    filing_date = indexes.DateField(model_attr='filing_date', null=True)
    publication_date = indexes.DateField(model_attr='publication_date', null=True)
    publication_no = indexes.CharField(model_attr="publication_no")
    patent_date = indexes.DateField(model_attr='patent_date', null=True)
    patent_no = indexes.CharField(model_attr="patent_no")
    pre_decision_date = indexes.DateField(model_attr='pre_decision_date', null=True)
    pre_decision_no = indexes.CharField(model_attr="pre_decision_no", null=True)
    re_examine_date = indexes.DateField(model_attr='re_examine_date', null=True)
    examination_date = indexes.DateField(model_attr='examination_date', null=True)
    patent_term = indexes.DateField(model_attr='patent_term', null=True)
    final_patent_term = indexes.DateField(model_attr='final_patent_term', null=True)
    certificate_no = indexes.CharField(model_attr="certificate_no")
    prio_application_no = indexes.CharField(model_attr="prio_application_no")
    prio_filing_date = indexes.DateField(model_attr='prio_filing_date', null=True)
    file_holder_position = indexes.CharField(model_attr="file_holder_position")
    IDS_information = indexes.CharField(model_attr="IDS_information")
    created = indexes.DateTimeField(model_attr='created')
    created_by = indexes.CharField(model_attr="created_by", null=True)
    remarks = indexes.CharField(model_attr="remarks")

    def get_model(self):
        return Patent

    def prepare_inventor(self, obj):
        return ["%s %s" % (item.chinese_name, item.english_name) for item in obj.inventor.all()]

    def prepare_agent(self, obj):
        if obj.agent:
            return "%s %s" % (obj.agent.agent_id, obj.agent.agent_title)

    def prepare_country(self, obj):
        return str(obj.country_template)

    def prepare_created_by(self, obj):
        if obj.created_by:
            return "%s %s" % (obj.created_by.get_username(), obj.created_by.get_full_name())
        else:
            return ""


class AgentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    agent_id = indexes.IntegerField(model_attr="agent_id")
    agent_title = indexes.CharField(model_attr="agent_title")
    country = indexes.CharField(model_attr="country")
    address = indexes.CharField(model_attr="address")
    beneficiary_name = indexes.CharField(model_attr="beneficiary_name")
    remittance_bank = indexes.CharField(model_attr="remittance_bank")
    beneficiary_no = indexes.CharField(model_attr="beneficiary_no")
    contact_person_name = indexes.CharField(model_attr="contact_person_name")
    contact_person_phone_number = indexes.CharField(model_attr="contact_person_phone_number")
    contact_person_email = indexes.CharField(model_attr="contact_person_email")
    created = indexes.DateTimeField(model_attr='created')
    created_by = indexes.CharField(model_attr="created_by", null=True)
    remarks = indexes.CharField(model_attr="remarks")

    def get_model(self):
        return Agent

    def prepare_created_by(self, obj):
        if obj.created_by:
            return "%s %s" % (obj.created_by.get_username(), obj.created_by.get_full_name())
        else:
            return ""


class InventorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    chinese_name = indexes.CharField(model_attr="chinese_name")
    english_name = indexes.CharField(model_attr="english_name")
    country = indexes.CharField(model_attr="country")
    post_address = indexes.CharField(model_attr="post_address")
    english_address = indexes.CharField(model_attr="english_address")
    phone_number = indexes.CharField(model_attr="phone_number")
    id_number = indexes.CharField(model_attr="id_number")
    email = indexes.CharField(model_attr="email")
    created = indexes.DateTimeField(model_attr='created')
    created_by = indexes.CharField(model_attr="created_by", null=True)
    remarks = indexes.CharField(model_attr="remarks")

    def get_model(self):
        return Inventor

    def prepare_created_by(self, obj):
        if obj.created_by:
            return "%s %s" % (obj.created_by.get_username(), obj.created_by.get_full_name())
        else:
            return ""


class ProposalIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    proposal_id = indexes.CharField(model_attr="proposal_id")
    chinese_title = indexes.CharField(model_attr="chinese_title")
    english_title = indexes.CharField(model_attr="english_title")
    inventors = indexes.MultiValueField()
    department = indexes.CharField(model_attr="department")
    category = indexes.CharField(model_attr="category")
    proposal_date = indexes.DateField(model_attr='proposal_date', null=True)
    country = indexes.CharField(model_attr="country")
    abstract = indexes.CharField(model_attr="abstract")
    performance = indexes.CharField(model_attr="performance")
    appraisal_date = indexes.DateField(model_attr='appraisal_date', null=True)
    created = indexes.DateTimeField(model_attr='created')
    created_by = indexes.CharField(model_attr="created_by", null=True)
    remarks = indexes.CharField(model_attr="remarks")

    def get_model(self):
        return Proposal

    def prepare_inventor(self, obj):
        return ["%s %s" % (item.chinese_name, item.english_name) for item in obj.inventors.all()]

    def prepare_created_by(self, obj):
        if obj.created_by:
            return "%s %s" % (obj.created_by.get_username(), obj.created_by.get_full_name())
        else:
            return ""
