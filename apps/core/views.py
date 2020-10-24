from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"
    login_url = '/login'


def handler404(request, exception):
    """ Set the 404 error page """
    return render(request, '404.html', status=404)


def handler500(request):
    """ Set the 500 error page """
    return render(request, '500.html', status=500)


def handler403(request, exception):
    """ Set the 403 error page """
    return render(request, '403.html', status=403)


def handler400(request, exception):
    """ Set the 400 error page """
    return render(request, '400.html', status=400)
