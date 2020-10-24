from django import forms

from .models import Representative


class RepresentativeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RepresentativeForm, self).__init__(*args, **kwargs)
        self.fields['last_status_date'].widget.attrs = { 'class': 'date', 'data-toggle': 'date-picker', 'data-single-date-picker': 'true' }
        self.fields['last_hire_date'].widget.attrs = { 'class': 'date', 'data-toggle': 'date-picker', 'data-single-date-picker': 'true' }

    class Meta:
        model = Representative
        fields = '__all__'
