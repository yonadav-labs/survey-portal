from itertools import chain

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Div, Fieldset
from django.utils.encoding import force_str
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

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


class SortedCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    def build_attrs(self, attrs=None, **kwargs):
        attrs = dict(attrs or {}, **kwargs)
        attrs = super(SortedCheckboxSelectMultiple, self).build_attrs(attrs)
        return attrs

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)

        # Normalize to strings
        str_values = [force_str(v) for v in value]

        selected = []
        unselected = []

        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_id = conditional_escape(final_attrs['id'])
            else:
                label_id = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_str(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_str(option_label))
            item = {
                'label_id': label_id,
                'rendered_cb': rendered_cb,
                'option_label': option_label,
                'option_value': option_value
            }
            if option_value in str_values:
                selected.append(item)
            else:
                unselected.append(item)

        # Reorder `selected` array according str_values which is a set of `option_value`s in the
        # order they should be shown on screen
        ordered = []
        for s in str_values:
            for select in selected:
                if s == select['option_value']:
                    ordered.append(select)
        selected = ordered

        html = render_to_string(
            'audits/sorted_checkbox_select_multiple_widget.html',
            {'selected': selected, 'unselected': unselected})
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if isinstance(value, (str,)):
            return [v for v in value.split(',') if v]
        return value


class SortedMultipleChoiceField(forms.ModelMultipleChoiceField):
    widget = SortedCheckboxSelectMultiple


class TemplateForm(forms.ModelForm):
    questions = SortedMultipleChoiceField(
        queryset=Question.objects.filter(enabled=True),
        required=False
    )

    category = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-2'}),
        required=False
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-2'})
    )

    enabled = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'checkboxinput custom-control-input'}),
        required=False
    )

    class Meta:
        model = Template
        fields = '__all__'
