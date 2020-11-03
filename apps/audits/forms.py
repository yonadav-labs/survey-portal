from django import forms

from apps.representatives.models import *
from .models import *


class AuditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AuditForm, self).__init__(*args, **kwargs)
        self.fields['call_date'].widget.attrs = { 'class': 'date', 'data-toggle': 'date-picker', 'data-single-date-picker': 'true' }
        self.fields['representative'].queryset = Representative.objects.filter(status="ACTIVE")
        self.fields['template'].queryset = Template.objects.filter(enabled=True)

    class Meta:
        model = Audit
        fields = '__all__'
