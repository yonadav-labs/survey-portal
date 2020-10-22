from django.urls import path

from . import views

app_name = 'representatives'

urlpatterns = [
    path('', views.RepresentativeList.as_view(), name='list'),
    path('create', views.RepresentativeCreate.as_view(), name='create'),
    path('<uuid:pk>', views.RepresentativeDetail.as_view(), name='detail'),
    path('<uuid:pk>/update', views.RepresentativeUpdate.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.RepresentativeDelete.as_view(), name='delete'),
]