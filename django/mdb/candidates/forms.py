# coding: utf-8
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'email',
            'name',
            'comment',
        ]

class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()