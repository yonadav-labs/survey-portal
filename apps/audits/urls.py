from django.urls import path

from . import views

app_name = 'audits'

urlpatterns = [
    path('', views.AuditList.as_view(), name='list'),
    path('create', views.AuditCreate.as_view(), name='create'),
    path('<uuid:pk>', views.AuditDetail.as_view(), name='detail'),
    path('<uuid:pk>/update', views.AuditUpdate.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.AuditDelete.as_view(), name='delete'),
    path('answer', views.AnswerList.as_view(), name='answer-list'),
    path('answer/create', views.AnswerCreate.as_view(), name='answer-create'),
    path('answer/<uuid:pk>', views.AnswerDetail.as_view(), name='answer-detail'),
    path('answer/<uuid:pk>/update', views.AnswerUpdate.as_view(), name='answer-update'),
    path('answer/<uuid:pk>/delete/', views.AnswerDelete.as_view(), name='answer-delete'),
    path('question', views.QuestionList.as_view(), name='question-list'),
    path('question/create', views.QuestionCreate.as_view(), name='question-create'),
    path('question/<uuid:pk>', views.QuestionDetail.as_view(), name='question-detail'),
    path('question/<uuid:pk>/update', views.QuestionUpdate.as_view(), name='question-update'),
    path('question/<uuid:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
    path('template', views.TemplateList.as_view(), name='template-list'),
    path('template/create', views.TemplateCreate.as_view(), name='template-create'),
    path('template/<uuid:pk>', views.TemplateDetail.as_view(), name='template-detail'),
    path('template/<uuid:pk>/update', views.TemplateUpdate.as_view(), name='template-update'),
    path('template/<uuid:pk>/delete/', views.TemplateDelete.as_view(), name='template-delete'),
]