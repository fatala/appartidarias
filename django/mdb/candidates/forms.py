# coding: utf-8
from django import forms

from .models import Comment, Contact


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'email',
            'name',
            'comment',
        ]

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            'email',
            'name',
            'message',
        ]