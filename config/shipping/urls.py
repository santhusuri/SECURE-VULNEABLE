from django.urls import path
from . import views

app_name = 'shipping'

urlpatterns = [
    path('details/<int:order_id>/', views.shipping_details, name='shipping_details'),
]
