from django.urls import path
from .views import toggle_mode
from . import views

urlpatterns = [
    path('search/', views.search_view, name='search'),
    path('upload/', views.upload_view, name='upload'),
    path('toggle_mode/', toggle_mode, name='toggle_mode'),
]