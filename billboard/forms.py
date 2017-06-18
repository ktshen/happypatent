from django import forms
from proposals.utils import file_validate
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PostModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
                            max_length=100)
    file = forms.FileField(label="Files",
                           widget=forms.ClearableFileInput(attrs={'multiple': True}),
                           validators=[file_validate],
                           required=False)

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'submit', css_class='btn btn-info'))

    class Meta:
        model = Post
        fields = ["title", "text", "file"]


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

