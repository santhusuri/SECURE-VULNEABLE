
from django.urls import path
from . import views
from .views import ids_dashboard, airs_dashboard

urlpatterns = [
    # Demo views
    path('search/', views.search_view, name='search'),
    path('upload/', views.upload_view, name='upload'),

    # Toggle mode (Secure / Vulnerable)
    path('toggle_mode/', views.toggle_mode_api, name='toggle_mode'),
    path('ids_dashboard/', ids_dashboard, name='ids_dashboard'),
    path('airs_dashboard/', airs_dashboard, name='airs_dashboard'),

]
