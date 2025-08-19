from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from django.views.decorators.http import require_POST

# ======================================================
# CART APP VIEWS
# ======================================================

# ======================================================
# Utility Functions
# ======================================================
def get_cart(request):
    """
    Retrieves the shopping cart from session.
    If no cart exists, returns an empty dict.
    """
    return request.session.get('cart', {})


def save_cart(request, cart):
    """
    Saves the updated cart into session.
    """
    request.session['cart'] = cart


# ======================================================
# View Cart
# ======================================================
def cart_view(request):
    """
    Displays the current shopping cart.
    - Retrieves cart from session (dict structure).
    - Calculates total cost of items.
    """
    cart = get_cart(request)
    total = sum(item['price'] * item['qty'] for item in cart.values())
    return render(request, 'cart/cart_view.html', {
        'cart': cart,
        'total': total
    })


# ======================================================
# Add Product to Cart
# ======================================================
def add_to_cart(request, product_id):
    """
    Adds a product to the shopping cart.
    Behavior depends on current mode:
    - Secure mode:
        Uses get_object_or_404 for validation.
        Ensures only real product IDs are allowed.
    - Vulnerable mode:
        Skips validation (intentionally insecure).
        Demonstrates ID/price tampering possibilities.
    """
    mode = request.session.get('mode', 'secure')
    cart = get_cart(request)

    if mode == 'secure':
        # -----------------------------
        # Secure Add-to-Cart
        # -----------------------------
        product = get_object_or_404(Product, id=product_id)

    elif mode == 'vulnerable':
        # -----------------------------
        # Vulnerable Add-to-Cart
        # -----------------------------
        # ⚠ No error handling or validation
        #    - Product IDs may be tampered
        #    - Prices could be manipulated in the frontend
        product = Product.objects.get(id=product_id)

    # Add or update product in cart
    if str(product.id) not in cart:
        cart[str(product.id)] = {
            'name': product.name,
            'price': float(product.price),
            'qty': 1
        }
    else:
        cart[str(product.id)]['qty'] += 1

    # Save back to session
    save_cart(request, cart)

    # Show different messages for secure vs vulnerable
    if mode == 'secure':
        messages.success(request, f"{product.name} added to cart.")
    else:
        messages.warning(request, f"(Vulnerable) {product.name} added to cart without checks.")

    return redirect('cart:cart_view')


# ======================================================
# Remove Product from Cart
# ======================================================
def remove_from_cart(request, product_id):
    """
    Removes a specific product from the shopping cart.
    """
    cart = get_cart(request)
    if str(product_id) in cart:
        del cart[str(product_id)]
        save_cart(request, cart)
        messages.info(request, "Item removed from cart.")
    return redirect('cart:cart_view')


# ======================================================
# Clear Entire Cart
# ======================================================
def clear_cart(request):
    """
    Empties the entire shopping cart.
    """
    save_cart(request, {})
    messages.info(request, "Cart cleared.")
    return redirect('cart:cart_view')




@require_POST
def update_quantity(request, id):
    product = get_object_or_404(Product, id=id)
    action = request.POST.get('action')
    cart = request.session.get('cart', {})

    # Get current quantity or 0
    current_qty = cart.get(str(id), {}).get('qty', 0)

    if action == 'increase':
        new_qty = current_qty + 1
    elif action == 'decrease':
        new_qty = current_qty - 1 if current_qty > 1 else 1  # minimum qty = 1
    else:
        # If invalid action, redirect without change
        return redirect('cart:view_cart')  # Replace with your cart view name

    # Update cart data
    if new_qty >= 1:
        cart[str(id)]['qty'] = new_qty
    else:
        # If qty drops below 1, remove the item from cart
        cart.pop(str(id), None)

    # Save back to session
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart:view_cart')  # Replace with your cart URL name
