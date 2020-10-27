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


class InfractionList(LoginRequiredMixin, ListView):
    model = Infraction
    login_url = '/login'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        status = self.request.GET.get('status', '')

        q = Q(first_name__icontains=keyword) \
          | Q(last_name__icontains=keyword) \
          | Q(email__icontains=keyword)

        if status:
            q &= Q(status=status)

        return Infraction.objects.filter(q).order_by('first_name')

    def get_context_data(self, **kwargs):
        context = super(InfractionList, self).get_context_data(**kwargs)
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


class InfractionDetail(LoginRequiredMixin, DetailView):
    model = Infraction
    context_object_name = 'entity'
    login_url = '/login'

    @method_decorator(permission_required('infractions.view_representative', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(InfractionDetail, self).dispatch(request)


class InfractionCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Infraction
    success_url = reverse_lazy('infractions:list')
    success_message = 'Infraction created successfully.'
    login_url = '/login'
    form_class = InfractionForm

    @method_decorator(permission_required('infractions.add_representative', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(InfractionCreate, self).dispatch(request)


class InfractionUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Infraction
    context_object_name = 'entity'
    success_url = reverse_lazy('infractions:list')
    success_message = 'Infraction updated successfully.'
    login_url = '/login'
    form_class = InfractionForm

    @method_decorator(permission_required('infractions.change_representative', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(InfractionUpdate, self).dispatch(request)


class InfractionDelete(LoginRequiredMixin, DeleteView):
    model = Infraction
    success_url = reverse_lazy('infractions:list')
    success_message = 'Infraction deleted successfully.'
    login_url = '/login'

    @method_decorator(permission_required('infractions.delete_representative', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(InfractionDelete, self).dispatch(request)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(InfractionDelete, self).delete(request, *args, **kwargs)


# Infraction Type Views
class InfractionTypeList(LoginRequiredMixin, ListView):
    model = Infraction
    login_url = '/login'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        enabled = self.request.GET.get('enabled', '') == "true"

        q = Q(name__icontains=keyword)

        if enabled:
            q &= Q(enabled=enabled)

        return InfractionType.objects.filter(q).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(InfractionTypeList, self).get_context_data(**kwargs)
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


class InfractionTypeDetail(LoginRequiredMixin, DetailView):
    model = InfractionType
    context_object_name = 'entity'
    login_url = '/login'

    @method_decorator(permission_required('infractions.view_representative', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(InfractionDetail, self).dispatch(request)


class InfractionTypeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = InfractionType
    success_url = reverse_lazy('infractions:list')
    success_message = 'Infraction created successfully.'
    login_url = '/login'
    # form_class = InfractionForm

    @method_decorator(permission_required('infractions.add_representative', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(InfractionCreate, self).dispatch(request)


class InfractionTypeUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = InfractionType
    context_object_name = 'entity'
    success_url = reverse_lazy('infractions:list')
    success_message = 'Infraction updated successfully.'
    login_url = '/login'
    # form_class = InfractionForm

    @method_decorator(permission_required('infractions.change_representative', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(InfractionUpdate, self).dispatch(request)


class InfractionTypeDelete(LoginRequiredMixin, DeleteView):
    model = InfractionType
    success_url = reverse_lazy('infractions:list')
    success_message = 'Infraction deleted successfully.'
    login_url = '/login'

    @method_decorator(permission_required('infractions.delete_representative', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(InfractionDelete, self).dispatch(request)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(InfractionDelete, self).delete(request, *args, **kwargs)
