from django import forms

from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
                            max_length=100)
    class Meta:
        model = Post
        fields = ["title", "text"]


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

