from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from .models import *
from .forms import *


### ChoiceAnswer Viewsets ###

class AnswerList(LoginRequiredMixin, ListView):
    model = ChoiceAnswer
    login_url = '/login'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        enabled = self.request.GET.get('enabled') == 'true'

        q = Q(name__icontains=keyword)

        if enabled:
            q &= Q(enabled=enabled)

        return ChoiceAnswer.objects.filter(q).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(AnswerList, self).get_context_data(**kwargs)
        entities = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(entities, self.paginate_by)

        try:
            entities = paginator.page(page)
        except PageNotAnInteger:
            entities = paginator.page(1)
        except EmptyPage:
            entities = paginator.page(paginator.num_pages)
        context[self.context_object_name] = entities

        return context


class AnswerDetail(LoginRequiredMixin, DetailView):
    model = ChoiceAnswer
    context_object_name = 'entity'
    login_url = '/login'

    @method_decorator(permission_required('audits.view_choiceanswer', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AnswerDetail, self).dispatch(request)


class AnswerCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ChoiceAnswer
    success_url = reverse_lazy('audits:answer-list')
    success_message = 'Answer created successfully.'
    login_url = '/login'
    # form_class = AnswerForm
    fields = '__all__'

    @method_decorator(permission_required('audits.add_choiceanswer', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AnswerCreate, self).dispatch(request)


class AnswerUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ChoiceAnswer
    context_object_name = 'entity'
    success_url = reverse_lazy('audits:answer-list')
    success_message = 'Answer updated successfully.'
    login_url = '/login'
    # form_class = AnswerForm
    fields = '__all__'

    @method_decorator(permission_required('audits.change_choiceanswer', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AnswerUpdate, self).dispatch(request)


class AnswerDelete(LoginRequiredMixin, DeleteView):
    model = ChoiceAnswer
    success_url = reverse_lazy('audits:answer-list')
    success_message = 'Answer deleted successfully.'
    login_url = '/login'

    @method_decorator(permission_required('audits.delete_choiceanswer', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AnswerDelete, self).dispatch(request)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AnswerDelete, self).delete(request, *args, **kwargs)


### Question Viewsets ###

class QuestionList(LoginRequiredMixin, ListView):
    model = Question
    login_url = '/login'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        enabled = self.request.GET.get('enabled') == 'true'

        q = Q(name__icontains=keyword)

        if enabled:
            q &= Q(enabled=enabled)

        return Question.objects.filter(q).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        entities = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(entities, self.paginate_by)

        try:
            entities = paginator.page(page)
        except PageNotAnInteger:
            entities = paginator.page(1)
        except EmptyPage:
            entities = paginator.page(paginator.num_pages)
        context[self.context_object_name] = entities

        return context


class QuestionDetail(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'entity'
    login_url = '/login'

    @method_decorator(permission_required('audits.view_question', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionDetail, self).dispatch(request)


class QuestionCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Question
    success_url = reverse_lazy('audits:list')
    success_message = 'Question created successfully.'
    login_url = '/login'
    # form_class = QuestionForm

    @method_decorator(permission_required('audits.add_question', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionCreate, self).dispatch(request)


class QuestionUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Question
    context_object_name = 'entity'
    success_url = reverse_lazy('audits:list')
    success_message = 'Question updated successfully.'
    login_url = '/login'
    # form_class = QuestionForm

    @method_decorator(permission_required('audits.change_question', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionUpdate, self).dispatch(request)


class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('audits:list')
    success_message = 'Question deleted successfully.'
    login_url = '/login'

    @method_decorator(permission_required('audits.delete_question', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionDelete, self).dispatch(request)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(QuestionDelete, self).delete(request, *args, **kwargs)


### TemplateList Viewsets ###

class TemplateList(LoginRequiredMixin, ListView):
    model = Template
    login_url = '/login'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        enabled = self.request.GET.get('enabled') == 'true'

        q = Q(name__icontains=keyword)

        if enabled:
            q &= Q(enabled=enabled)

        return Template.objects.filter(q).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(TemplateList, self).get_context_data(**kwargs)
        entities = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(entities, self.paginate_by)

        try:
            entities = paginator.page(page)
        except PageNotAnInteger:
            entities = paginator.page(1)
        except EmptyPage:
            entities = paginator.page(paginator.num_pages)
        context[self.context_object_name] = entities

        return context


class TemplateDetail(LoginRequiredMixin, DetailView):
    model = Template
    context_object_name = 'entity'
    login_url = '/login'

    @method_decorator(permission_required('audits.view_template', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateDetail, self).dispatch(request)


class TemplateCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Template
    success_url = reverse_lazy('audits:list')
    success_message = 'Template created successfully.'
    login_url = '/login'
    # form_class = TemplateForm

    @method_decorator(permission_required('audits.add_template', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateCreate, self).dispatch(request)


class TemplateUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Template
    context_object_name = 'entity'
    success_url = reverse_lazy('audits:list')
    success_message = 'Template updated successfully.'
    login_url = '/login'
    # form_class = TemplateForm

    @method_decorator(permission_required('audits.change_template', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateUpdate, self).dispatch(request)


class TemplateDelete(LoginRequiredMixin, DeleteView):
    model = Template
    success_url = reverse_lazy('audits:list')
    success_message = 'Template deleted successfully.'
    login_url = '/login'

    @method_decorator(permission_required('audits.delete_template', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateDelete, self).dispatch(request)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TemplateDelete, self).delete(request, *args, **kwargs)


### AuditList Viewsets ###

class AuditList(LoginRequiredMixin, ListView):
    model = Audit
    login_url = '/login'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')

        q = Q(representative__first_name__icontains=keyword) \
          | Q(representative__last_name__icontains=keyword) \
          | Q(representative__email__icontains=keyword)

        return Audit.objects.filter(q).order_by('representative__first_name')

    def get_context_data(self, **kwargs):
        context = super(AuditList, self).get_context_data(**kwargs)
        entities = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(entities, self.paginate_by)

        try:
            entities = paginator.page(page)
        except PageNotAnInteger:
            entities = paginator.page(1)
        except EmptyPage:
            entities = paginator.page(paginator.num_pages)
        context[self.context_object_name] = entities

        return context


class AuditDetail(LoginRequiredMixin, DetailView):
    model = Audit
    context_object_name = 'entity'
    login_url = '/login'

    @method_decorator(permission_required('audits.view_audit', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AuditDetail, self).dispatch(request)


class AuditCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Audit
    success_url = reverse_lazy('audits:list')
    success_message = 'Audit created successfully.'
    login_url = '/login'
    # form_class = AuditForm

    @method_decorator(permission_required('audits.add_audit', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AuditCreate, self).dispatch(request)


class AuditUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Audit
    context_object_name = 'entity'
    success_url = reverse_lazy('audits:list')
    success_message = 'Audit updated successfully.'
    login_url = '/login'
    # form_class = AuditForm

    @method_decorator(permission_required('audits.change_audit', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AuditUpdate, self).dispatch(request)


class AuditDelete(LoginRequiredMixin, DeleteView):
    model = Audit
    success_url = reverse_lazy('audits:list')
    success_message = 'Audit deleted successfully.'
    login_url = '/login'

    @method_decorator(permission_required('audits.delete_audit', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AuditDelete, self).dispatch(request)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AuditDelete, self).delete(request, *args, **kwargs)
