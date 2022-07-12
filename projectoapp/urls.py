from django.urls import path
from . import views

urlpatterns = [
    path('projecto/', views.index),
    path('projecto/projects/', views.project_list, name='project_list'),
    path('projecto/project/show/<str:Id>/', views.project_action, name='project_action'),
    path('projecto/project/update/<str:Id>/', views.project_update, name='project_update'),
    path('projecto/project/create/', views.project_create, name='project_create'),
    path('projecto/project/delete/<str:Id>/', views.project_delete, name='project_delete'),
    path('projecto/project/', views.project_search, name='project_search'),
    path('projecto/contact/', views.project_contact, name='project_contact')
]