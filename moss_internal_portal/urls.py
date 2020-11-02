"""moss_internal_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.core import views as core_views


handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'
handler403 = 'apps.core.views.handler403'
handler400 = 'apps.core.views.handler400'

urlpatterns = [
    path('', core_views.HomeView.as_view(), name='index'),
    path('', include('apps.accounts.urls')),
    path('representatives/', include('apps.representatives.urls')),
    path('infractions/', include('apps.infractions.urls')),
    path('audits/', include('apps.audits.urls')),
    path('superpanel/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
