from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main.html'), name='home'),     
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('airs_dashboard/', include(('airs_dashboard.urls', 'airs_dashboard'), namespace='airs_dashboard')),
    path('ids_dashboard/', include(('ids_dashboard.urls', 'ids_dashboard'), namespace='ids_dashboard')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('core/', include(('core.urls', 'core'), namespace='core')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('shipping/', include(('shipping.urls', 'shipping'), namespace='shipping')),

]

# This line adds media URL serving only when DEBUG=True (development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)