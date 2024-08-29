from . import models
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("title", "user", "content")
