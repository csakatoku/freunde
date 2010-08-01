# -*- coding: utf-8 -*-
from django import forms

class OpenSearchForm(forms.Form):
    count      = forms.IntegerField(min_value=1)
    startIndex = forms.IntegerField(min_value=0)
