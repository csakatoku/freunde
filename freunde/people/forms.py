# -*- coding: utf-8 -*-
from django import forms

class OpenSearchForm(forms.Form):
    count      = forms.IntegerField(min_value=1)
    startIndex = forms.IntegerField(min_value=0)
    filterBy   = forms.CharField(required=False)

    def clean_filterBy(self):
        value = self.cleaned_data.get('filterBy')
        if value and value != 'hasApp':
            raise forms.ValidationError("Unsupported value '%r' for the field filterBy" % value)
        return value
