from django import template
from apps.audits.models import *

register = template.Library()


@register.filter
def answer(question, audit):
    res = Response.objects.filter(question=question, audit=audit).first()
    if not res:
        return ''

    if question.type == 'CHOICE':
        return res.choice_answer.name if res.choice_answer else ''
    elif question.type == 'TEXT':
        return res.text_answer
    elif question.type == 'NUMBER':
        return res.number_answer
    elif question.type == 'YESNO':
        return 'Yes' if res.yesno_answer else 'No' if res.yesno_answer == False else ''


@register.filter
def checked_yes(question, audit):
    res = Response.objects.filter(question=question, audit=audit).first()
    if res and res.yesno_answer == True:
        return 'checked'

    return ''


@register.filter
def checked_no(question, audit):
    res = Response.objects.filter(question=question, audit=audit).first()
    if res and res.yesno_answer == False:
        return 'checked'

    return ''


@register.filter
def selected(val, answer):
    return 'selected' if val == answer.name else ''

