from haystack import indexes
from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    first_name = indexes.CharField(model_attr="first_name")
    last_name = indexes.CharField(model_attr="last_name")
    email = indexes.CharField(model_attr="email")
    id_number = indexes.CharField(model_attr="id_number")
    gender = indexes.CharField(model_attr="gender")
    county = indexes.CharField(model_attr="county")
    address = indexes.CharField(model_attr="address")
    home_number = indexes.CharField(model_attr="home_number")
    mobile_number = indexes.CharField(model_attr="mobile_number")
    office_number = indexes.CharField(model_attr="office_number")
    spouse_name = indexes.CharField(model_attr="spouse_name")
    education = indexes.CharField(model_attr="education")
    experience = indexes.CharField(model_attr="experience")
    remarks = indexes.CharField(model_attr="remarks")

    def get_model(self):
        return User
