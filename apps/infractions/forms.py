from django import forms

from .models import Infraction


class InfractionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InfractionForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs = { 'class': 'date', 'data-toggle': 'date-picker', 'data-single-date-picker': 'true' }

    class Meta:
        model = Infraction
        fields = '__all__'
