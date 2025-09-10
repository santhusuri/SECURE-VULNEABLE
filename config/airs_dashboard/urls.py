from django.urls import path
from . import views

urlpatterns = [
    path('', views.airs_dashboard, name='airs_dashboard'),
]
