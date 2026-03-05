from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('run-migration/', views.run_migration, name='run_migration'),
]