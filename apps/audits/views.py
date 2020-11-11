from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import model_to_dict

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
        enabled = self.request.GET.get('enabled')

        q = Q(name__icontains=keyword)

        if enabled:
            enabled = enabled == 'true'
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


class AnswerClone(View):
    form_class = AnswerForm
    template_name = 'audits/choiceanswer_form.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        entity = get_object_or_404(self.form_class.Meta.model, pk=pk)
        entity.id = None
        entity.name = entity.name + '_copy'
        form = self.form_class(initial=model_to_dict(entity))

        return render(request, self.template_name, locals())


### Question Viewsets ###

class QuestionList(LoginRequiredMixin, ListView):
    model = Question
    login_url = '/login'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        enabled = self.request.GET.get('enabled')

        q = Q(name__icontains=keyword)

        if enabled:
            enabled = enabled == 'true'
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
    success_url = reverse_lazy('audits:question-list')
    success_message = 'Question created successfully.'
    login_url = '/login'
    fields = '__all__'

    def get_form(self, *args, **kwargs):
        form = super(QuestionCreate, self).get_form(*args, **kwargs)
        form.fields['answers'].queryset = ChoiceAnswer.objects.filter(enabled=True)
        return form

    @method_decorator(permission_required('audits.add_question', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionCreate, self).dispatch(request)


class QuestionUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Question
    context_object_name = 'entity'
    success_url = reverse_lazy('audits:question-list')
    success_message = 'Question updated successfully.'
    login_url = '/login'
    fields = '__all__'

    def get_form(self, *args, **kwargs):
        form = super(QuestionUpdate, self).get_form(*args, **kwargs)
        form.fields['answers'].queryset = ChoiceAnswer.objects.filter(enabled=True)
        return form

    @method_decorator(permission_required('audits.change_question', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionUpdate, self).dispatch(request)


class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('audits:question-list')
    success_message = 'Question deleted successfully.'
    login_url = '/login'

    @method_decorator(permission_required('audits.delete_question', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionDelete, self).dispatch(request)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(QuestionDelete, self).delete(request, *args, **kwargs)


class QuestionClone(View):
    form_class = QuestionForm
    template_name = 'audits/question_form.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        entity = get_object_or_404(self.form_class.Meta.model, pk=pk)
        entity.id = None
        entity.name = entity.name + '_copy'
        form = self.form_class(initial=model_to_dict(entity))

        return render(request, self.template_name, locals())


### TemplateList Viewsets ###

class TemplateList(LoginRequiredMixin, ListView):
    model = Template
    login_url = '/login'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        enabled = self.request.GET.get('enabled')

        q = Q(name__icontains=keyword)

        if enabled:
            enabled = enabled == 'true'
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
    form_class = TemplateForm
    success_url = reverse_lazy('audits:template-list')
    success_message = 'Template created successfully.'
    login_url = '/login'

    @method_decorator(permission_required('audits.add_template', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateCreate, self).dispatch(request)

    def form_valid(self, form):
        self.object = form.save()
        self.object.questions.clear()
        for question_id in self.request.POST.getlist('questions'):
            question = Question.objects.get(pk=question_id)
            self.object.questions.add(question)

        return redirect(self.success_url)


class TemplateUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Template
    form_class = TemplateForm
    context_object_name = 'entity'
    success_url = reverse_lazy('audits:template-list')
    success_message = 'Template updated successfully.'
    login_url = '/login'

    @method_decorator(permission_required('audits.change_template', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateUpdate, self).dispatch(request)

    def form_valid(self, form):
        self.object = form.save()
        self.object.questions.clear()
        for question_id in self.request.POST.getlist('questions'):
            question = Question.objects.get(pk=question_id)
            self.object.questions.add(question)

        return redirect(self.success_url)


class TemplateDelete(LoginRequiredMixin, DeleteView):
    model = Template
    success_url = reverse_lazy('audits:template-list')
    success_message = 'Template deleted successfully.'
    login_url = '/login'

    @method_decorator(permission_required('audits.delete_template', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateDelete, self).dispatch(request)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TemplateDelete, self).delete(request, *args, **kwargs)


class TemplateClone(View):
    form_class = TemplateForm
    template_name = 'audits/template_form.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        entity = get_object_or_404(self.form_class.Meta.model, pk=pk)
        entity.id = None
        entity.name = entity.name + '_copy'
        form = self.form_class(initial=model_to_dict(entity))

        return render(request, self.template_name, locals())


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
    form_class = AuditForm

    @method_decorator(permission_required('audits.add_audit', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AuditCreate, self).dispatch(request)

    def form_valid(self, form):
        self.object = form.save()
        meta_new_desc = self.request.POST.get('meta_new_desc', '').split('@$@')

        # add new files
        idx = 0
        for file in self.request.FILES.getlist('attachment-file'):
            name_parts = file.name.split('.')
            extension = name_parts[-1] if len(name_parts) > 1 else None
            description = meta_new_desc[idx]
            idx += 1
            self.object.attachments.create(
                file=file,
                name=file.name,
                file_extension=extension,
                description=description
            )

        return super().form_valid(form)


class AuditUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Audit
    context_object_name = 'entity'
    success_url = reverse_lazy('audits:list')
    success_message = 'Audit updated successfully.'
    login_url = '/login'
    form_class = AuditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_old_files'] = '@$@'.join([ii.name for ii in self.object.attachments.all()])
        context['meta_old_desc'] = '@$@'.join([ii.description or '' for ii in self.object.attachments.all()])

        return context

    @method_decorator(permission_required('audits.change_audit', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(AuditUpdate, self).dispatch(request)

    def form_valid(self, form):
        self.object = form.save()
        meta_old_files = self.request.POST.get('meta_old_files').split('@$@')
        meta_old_desc = self.request.POST.get('meta_old_desc').split('@$@')
        meta_new_desc = self.request.POST.get('meta_new_desc', '').split('@$@')

        # sync old files
        for file in self.object.attachments.all():
            if file.name not in meta_old_files:
                file.delete()
            else:
                idx = meta_old_files.index(file.name)
                if meta_old_desc[idx] != file.description:
                    file.description = meta_old_desc[idx]
                    file.save()

        # add new files
        idx = 0
        for file in self.request.FILES.getlist('attachment-file'):
            name_parts = file.name.split('.')
            extension = name_parts[-1] if len(name_parts) > 1 else None
            description = meta_new_desc[idx]
            idx += 1
            self.object.attachments.create(
                file=file,
                name=file.name,
                file_extension=extension,
                description=description
            )

        return super().form_valid(form)


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


class AuditFill(View):

    def get(self, request, *args, **kwargs):
        audit_id = kwargs.get('pk')
        audit = get_object_or_404(Audit, pk=audit_id)

        return render(request, 'audits/audit_fill.html', locals())

    def post(self, request, *args, **kwargs):
        audit_id = kwargs.get('pk')
        audit = get_object_or_404(Audit, pk=audit_id)
        error_msg = []

        for question in audit.template.questions.all():
            res = request.POST.get(str(question.id)) or None

            if question.type == 'CHOICE':
                Response.objects.update_or_create(audit=audit, question=question, defaults={'choice_answer_id': res})
            elif question.type == 'TEXT':
                Response.objects.update_or_create(audit=audit, question=question, defaults={'text_answer': res})
            elif question.type == 'NUMBER':
                Response.objects.update_or_create(audit=audit, question=question, defaults={'number_answer': res})
            elif question.type == 'YESNO':
                res = res == 'true' if res else None
                Response.objects.update_or_create(audit=audit, question=question, defaults={'yesno_answer': res})

        if not error_msg:
            messages.success(self.request, "The audit answers saved successfully.")
            return redirect(reverse_lazy('audits:list'))

        return render(request, 'audits/audit_fill.html', locals())


class AuditClone(View):
    form_class = AuditForm
    template_name = 'audits/audit_form.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        entity = get_object_or_404(self.form_class.Meta.model, pk=pk)
        entity.id = None
        entity.call_date = None
        entity.notes = None
        form = self.form_class(initial=model_to_dict(entity))

        return render(request, self.template_name, locals())
