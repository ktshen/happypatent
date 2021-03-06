from django import forms
from fileattachments.utils import file_validate
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Fieldset,Div,ButtonHolder


class PostModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
                            max_length=100)

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout=Layout(
            Fieldset(
                "",
               Div(
                   "title",
                   "text",
                    css_class='box-body'
                ),
                Div(
                    Div(
                        ButtonHolder(Submit('save', 'submit',css_class='btn btn-primary pull-right')),
                        css_class='col-sm-12 '
                    ),
                    css_class='box-footer'
                )
            )
        )
    class Meta:
        model = Post
        fields = ["title", "text"]


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

