from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Representative


class RepresentativeList(LoginRequiredMixin, ListView):
    model = Representative
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        return Representative.objects.order_by('first_name')

    def get_context_data(self, **kwargs):
        context = super(RepresentativeList, self).get_context_data(**kwargs)
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


class RepresentativeDetail(DetailView):
    model = Representative
    context_object_name = 'entity'


class RepresentativeCreate(CreateView):
    model = Representative
    fields = '__all__'
    success_url = reverse_lazy('representatives:list')


class RepresentativeUpdate(UpdateView):
    model = Representative
    fields = '__all__'
    context_object_name = 'entity'
    success_url = reverse_lazy('representatives:list')


class RepresentativeDelete(DeleteView):
    model = Representative
    success_url = reverse_lazy('representatives:list')
