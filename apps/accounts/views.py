from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect


class LoginView(TemplateView):
    template_name = "accounts/login.html"


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
