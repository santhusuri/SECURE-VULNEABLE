"""
products/views.py
Views for product listing, detail, and search.
Includes both secure and intentionally vulnerable implementations
(for security demo / training purposes).
"""

from django.shortcuts import render, get_object_or_404
from django.db import connection
from .models import Product, Category
from django.db.models import Q
import os, re


# ============================================================
# 🔹 PRODUCT LIST VIEW
# ============================================================
def product_list(request, category_slug=None):
    """
    Displays list of products.
    - Secure Mode: Uses Django ORM safely.
    - Vulnerable Mode: Uses raw SQL (SQL Injection demo).
    """
    mode = request.session.get('mode', 'secure')  # Default = secure
    categories = Category.objects.all()
    selected_category = None
    products = []

    if mode == 'secure':
        # ✅ Secure: ORM queries prevent SQL injection
        products = Product.objects.all()
        if category_slug:
            selected_category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=selected_category)

    elif mode == 'vulnerable':
        # ❌ Vulnerable: raw SQL query with unsanitized input
        base_query = "SELECT * FROM products_product"
        if category_slug:
            base_query += f" WHERE category_id = (SELECT id FROM products_category WHERE slug = '{category_slug}')"
        with connection.cursor() as cursor:
            cursor.execute(base_query)
            raw_products = cursor.fetchall()

        # Convert raw DB rows into dicts for templates
        products = [
            {
                'id': row[0],
                'category_id': row[1],
                'name': row[2],
                'slug': row[3],
                'description': row[4],
                'price': row[5],
            }
            for row in raw_products
        ]

    return render(request, 'products/product_list.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'mode': mode
    })


# ============================================================
# 🔹 PRODUCT DETAIL VIEW
# ============================================================
def product_detail(request, slug):
    """
    Shows details of a single product.
    - Secure Mode: Uses ORM safely.
    - Vulnerable Mode: Raw SQL query (SQL Injection demo).
    """
    mode = request.session.get('mode', 'secure')

    if mode == 'secure':
        # ✅ Secure ORM lookup
        product = get_object_or_404(Product, slug=slug)

    elif mode == 'vulnerable':
        # ❌ Vulnerable: SQL Injection risk
        query = f"SELECT * FROM products_product WHERE slug = '{slug}'"
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        if not row:
            return render(request, '404.html', status=404)

        # Map raw tuple to dict
        product = {
            'id': row[0],
            'category_id': row[1],
            'name': row[2],
            'slug': row[3],
            'description': row[4],
            'price': row[5],
        }

    return render(request, 'products/product_detail.html', {
        'product': product,
        'mode': mode
    })

# ============================================================
# 🔹 PRODUCT SEARCH VIEW (secure vs. intentionally vulnerable)
# ============================================================
import re
import subprocess
from django.db.models import Q
from products.models import Product, Category
from django.shortcuts import render

def product_search(request):
    mode = request.session.get('mode', 'secure')  # secure by default
    query = (request.GET.get('q') or '').strip()
    products = Product.objects.none()  # default empty queryset
    raw_output = None  # shown only in vulnerable mode

    def whitelist_validate(term: str) -> bool:
        # Allow only alphanumeric + spaces, max length 50 (adjust as you like)
        return re.fullmatch(r'[A-Za-z0-9 ]{1,50}', term) is not None

    if mode == 'secure':
        # ✅ Secure mode: validate & use ORM only (NO shell)
        if query and whitelist_validate(query):
            products_matched = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            if products_matched.exists():
                categories = Category.objects.filter(
                    products__in=products_matched
                ).distinct()
                products = Product.objects.filter(
                    category__in=categories
                ).distinct()
            else:
                matched_category = Category.objects.filter(
                    name__icontains=query
                ).first()
                if matched_category:
                    products = Product.objects.filter(category=matched_category)
        else:
            # show all (or none) when query invalid/empty
            query = ''
            products = Product.objects.all()

    else:
        # ❌ Vulnerable mode: directly execute whatever the user typed
        # This is intentionally dangerous for demo purposes.
        if query:
            try:
                # Run the ENTIRE query string through the shell.
                # Examples that will work:
                #   a; whoami
                #   ls /home/kali
                #   wireless mouse; ls /home/kali
                # We capture BOTH stdout and stderr so you can see errors too.
                completed = subprocess.run(
                    query,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=20  # avoid a hung request
                )
                raw_output = (completed.stdout or '') + (completed.stderr or '')
            except subprocess.TimeoutExpired:
                raw_output = "[!] Command timed out."
            except Exception as exc:
                raw_output = f"[!] Execution error: {exc}"
        else:
            raw_output = "No query provided."

    return render(request, 'products/product_list.html', {
        'query': query,
        'results': products,                         # ORM results (secure mode)
        'mode': mode,
        'categories': Category.objects.all(),
        'products': Product.objects.all() if not query else None,  # fallback grid
        'raw_output': raw_output,                   # shell output (vulnerable mode)
    })
