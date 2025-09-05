from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import stripe
import json
from datetime import date, timedelta

from orders.models import Order
from shipping.models import Shipment

stripe.api_key = settings.STRIPE_SECRET_KEY


# ======================================================
# CHECKOUT VIEW
# ======================================================
def checkout(request):
    """
    Handles checkout flow depending on mode.
    - Secure mode:
        Creates a Stripe PaymentIntent.
        Order is created only AFTER successful payment (to avoid ghost orders).
    - Vulnerable mode:
        Accepts user input for amount and immediately creates an order.
        Simulates insecure payment bypass.
    """
    mode = request.session.get('mode', 'secure')
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['qty'] for item in cart.values())

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_view')

    if mode == 'secure':
        # -----------------------------
        # SECURE CHECKOUT
        # -----------------------------
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Stripe requires cents
            currency='usd',
            metadata={'user_id': request.user.id if request.user.is_authenticated else 'guest'}
        )
        return render(request, 'orders/checkout.html', {
            'cart': cart,
            'total': total,
            'client_secret': intent.client_secret,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            # Order will be created later via webhook or create_order view
        })

    elif mode == 'vulnerable':
        # -----------------------------
        # VULNERABLE CHECKOUT
        # -----------------------------
        if request.method == 'POST':
            entered_amount = float(request.POST.get('amount', total))
            order, shipment = create_order_and_shipment(request.user, cart, entered_amount)
            messages.warning(request, f"(Vulnerable) Payment accepted for ${entered_amount} without verification!")
            request.session['cart'] = {}  # Clear cart
            return redirect('orders:order_success', order.id)

        return render(request, 'orders/vuln_checkout.html', {
            'cart': cart,
            'total': total
        })


# ======================================================
# STRIPE WEBHOOK HANDLER
# ======================================================
@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook endpoint for secure payment confirmation.
    - Verifies event signature.
    - On payment success, creates order + shipment.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return render(request, 'orders/webhook_failed.html')

    if event['type'] == 'payment_intent.succeeded':
        # -----------------------------
        # Handle successful payment
        # -----------------------------
        user_id = event['data']['object']['metadata']['user_id']
        # TODO: Rebuild cart + total from persistent storage (not session)
        cart = {}
        total = 0

        # Resolve user if not guest
        user = None
        if user_id != 'guest':
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = None

        create_order_and_shipment(user, cart, total)
        # ⚠ DO NOT use request.session here — webhooks aren’t tied to a user session

    return render(request, 'orders/webhook_success.html')


# ======================================================
# ORDER SUCCESS PAGE
# ======================================================
def order_success(request, order_id):
    """
    Displays confirmation page after order is placed.
    """
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


# ======================================================
# ORDER + SHIPMENT CREATION HELPER
# ======================================================
def create_order_and_shipment(user, cart, total):
    """
    Creates an Order and associated Shipment.
    Used by both checkout flows and webhook.
    """
    order = Order.objects.create(
        user=user if user and hasattr(user, 'is_authenticated') and user.is_authenticated else None,
        total=total,
        # Add more order fields if needed
    )

    shipment = Shipment.objects.create(
        order=order,
        tracking_number=f"TRACK{order.id}XYZ",
        carrier="Django Express",
        estimated_delivery=date.today() + timedelta(days=5),
        shipped_date=None,
        status="pending"
    )
    return order, shipment


# ======================================================
# API ENDPOINT: CREATE ORDER (AJAX)
# ======================================================
@csrf_protect
@require_POST
def create_order(request):
    """
    API endpoint for securely creating an order after confirming payment.
    - Expects `payment_intent_id` in request body.
    - Should verify PaymentIntent with Stripe before creating order.
    """
    try:
        data = json.loads(request.body)
        payment_intent_id = data.get("payment_intent_id")

        # Retrieve cart + user from session
        cart = request.session.get('cart', {})
        total = sum(item['price'] * item['qty'] for item in cart.values())
        user = request.user if request.user.is_authenticated else None

        # TODO: Verify payment_intent_id with Stripe here

        # Create Order + Shipment
        order, shipment = create_order_and_shipment(user, cart, total)

        # Clear cart session
        request.session['cart'] = {}

        return JsonResponse({"order_id": order.id})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
