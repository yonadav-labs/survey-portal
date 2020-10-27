from django.urls import path

from . import views

app_name = 'infractions'

urlpatterns = [
    path('', views.InfractionList.as_view(), name='list'),
    path('create', views.InfractionCreate.as_view(), name='create'),
    path('<uuid:pk>', views.InfractionDetail.as_view(), name='detail'),
    path('<uuid:pk>/update', views.InfractionUpdate.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.InfractionDelete.as_view(), name='delete'),
    path('type', views.InfractionTypeList.as_view(), name='type-list'),
    path('type/create', views.InfractionTypeCreate.as_view(), name='type-create'),
    path('type/<uuid:pk>', views.InfractionTypeDetail.as_view(), name='type-detail'),
    path('type/<uuid:pk>/update', views.InfractionTypeUpdate.as_view(), name='type-update'),
    path('type/<uuid:pk>/delete/', views.InfractionTypeDelete.as_view(), name='type-delete'),
]