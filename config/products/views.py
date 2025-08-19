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
# 🔹 PRODUCT SEARCH VIEW
# ============================================================

from django.shortcuts import render
from products.models import Product, Category
from django.db.models import Q
import re

def product_search(request):
    mode = request.session.get('mode', 'secure')  # get current mode from session, defaults to 'secure'
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()  # default empty queryset

    def whitelist_validate(term):
        # Allow only alphanumeric characters and spaces, max length 50
        return re.fullmatch(r'[A-Za-z0-9 ]{1,50}', term) is not None

    if mode == 'secure':
        if query and whitelist_validate(query):
            # Find products matching the query in name or description
            products_matched = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            if products_matched.exists():
                # Get categories linked to matched products using 'products' related_name
                categories = Category.objects.filter(products__in=products_matched).distinct()
                # Retrieve all products in those categories
                products = Product.objects.filter(category__in=categories).distinct()
            else:
                # If no product matches, check if any category name matches the query
                matched_category = Category.objects.filter(name__icontains=query).first()
                if matched_category:
                    products = Product.objects.filter(category=matched_category)
        else:
            query = ''  # reset query if it fails validation
            products = Product.objects.all()  # optionally show all products or none
    else:
        # Vulnerable mode: no validation on input (intentional for demo)
        if query:
            products_matched = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            if products_matched.exists():
                categories = Category.objects.filter(products__in=products_matched).distinct()
                products = Product.objects.filter(category__in=categories).distinct()
            else:
                matched_category = Category.objects.filter(name__icontains=query).first()
                if matched_category:
                    products = Product.objects.filter(category=matched_category)
        else:
            products = Product.objects.all()

    return render(request, 'products/product_list.html', {
        'query': query,
        'results': products,
        'mode': mode,
        'categories': Category.objects.all(),
        'products': Product.objects.all() if not query else None,  # fallback
    })
