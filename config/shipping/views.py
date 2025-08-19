"""
shipping/views.py
Handles shipment tracking and shipping details.
"""

from django.shortcuts import render, get_object_or_404
from shipping.models import Shipment


# ============================================================
# 🔹 SHIPPING DETAILS VIEW
# ============================================================
def shipping_details(request, order_id):
    """
    Display shipping details for a given order.
    
    Args:
        request: HTTP request object
        order_id (int): ID of the order whose shipment details are needed
    
    Returns:
        Renders `shipping/shipment_detail.html` with shipment information.
    
    Raises:
        404: If no shipment exists for the given order_id
    """
    # ✅ Secure: uses Django ORM `get_object_or_404` to safely fetch shipment
    shipment = get_object_or_404(Shipment, order_id=order_id)

    return render(request, 'shipping/shipment_detail.html', {
        'shipment': shipment
    })
