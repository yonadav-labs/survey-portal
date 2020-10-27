from django import forms

from apps.representatives.models import *
from .models import *


class InfractionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InfractionForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs = { 'class': 'date', 'data-toggle': 'date-picker', 'data-single-date-picker': 'true' }
        self.fields['representative'].queryset = Representative.objects.filter(status="ACTIVE")
        self.fields['type'].queryset = InfractionType.objects.filter(enabled=True)

    class Meta:
        model = Infraction
        fields = '__all__'
