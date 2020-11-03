from django.db import models

from moss_internal_portal.mixins import UUIDPrimaryKeyMixin, CreatedModifiedMixin
from apps.representatives.models import Representative


class ChoiceAnswer(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    category = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=150)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    TYPE = (
        ('CHOICE', 'Choice'),
        ('NUMBER', 'Number'),
        ('TEXT', 'Text'),
        ('YESNO', 'Yes/No'),
    )
    category = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=50, choices=TYPE)
    answers = models.ManyToManyField(ChoiceAnswer, blank=True, verbose_name="Choice Answers")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Template(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    category = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=150)
    questions = models.ManyToManyField(Question, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Audit(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE, related_name='audits')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='audits')
    call_date = models.DateField()
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.representative)} - {str(self.template)}"


class Response(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    choice_answer = models.ForeignKey(ChoiceAnswer, on_delete=models.CASCADE, blank=True, null=True)
    text_answer = models.TextField(blank=True, null=True)
    number_answer = models.FloatField(blank=True, null=True)
    yesno_answer = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.audit.name


class Attachment(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    file_extension = models.CharField(max_length=10)
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField()

    def __str__(self):
        return self.name
