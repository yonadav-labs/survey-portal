from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Div, Fieldset

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


class AnswerForm(forms.ModelForm):
    class Meta:
        model = ChoiceAnswer
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class TemplateForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.filter(enabled=True),
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper['questions'].wrap(Field, data_plugin="dragula")

    class Meta:
        model = Template
        fields = '__all__'
