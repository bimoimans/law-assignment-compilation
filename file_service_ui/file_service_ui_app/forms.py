# -*- coding: utf-8 -*-
from django import forms

class FileForm(forms.Form):
    uploaded_file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
