from django.urls import path
from . import views

urlpatterns = [
    path('', views.ids_dashboard, name='ids_dashboard'),
]
