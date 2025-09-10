"""
products/views.py
Views for product listing, detail, search, reviews, and file uploads.
Supports secure and vulnerable modes.
Manual attacks in vulnerable mode are automatically logged to IDS/AIRS.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Category, Review
from django.core.files.storage import default_storage
import subprocess
import re

from core.logger import write_ids_log, write_airs_log


# ============================================================
# Helper function to log attacks
# ============================================================
def log_attack(request, action_desc):
    user_id = request.user.username if request.user.is_authenticated else "guest"
    write_ids_log(user_id, action_desc)
    write_airs_log("suspicious_activity")


# ============================================================
# PRODUCT LIST VIEW
# ============================================================
def product_list(request, category_slug=None):
    mode = request.session.get('mode', 'secure')
    categories = Category.objects.all()
    selected_category = None
    products = []

    if mode == 'secure':
        products = Product.objects.all()
        if category_slug:
            selected_category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=selected_category)
    else:
        # Vulnerable: raw SQL
        base_query = "SELECT * FROM products_product"
        if category_slug:
            base_query += f" WHERE category_id = (SELECT id FROM products_category WHERE slug = '{category_slug}')"
        with connection.cursor() as cursor:
            cursor.execute(base_query)
            raw_products = cursor.fetchall()
        products = [
            {'id': row[0],'category_id': row[1],'name': row[2],'slug': row[3],'description': row[4],'price': row[5]}
            for row in raw_products
        ]

    return render(request, 'products/product_list.html',{
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'mode': mode
    })


# ============================================================
# PRODUCT DETAIL VIEW
# ============================================================
@login_required
def product_detail(request, slug):
    mode = request.session.get('mode', 'secure')
    product = None

    if mode == 'secure':
        product = get_object_or_404(Product, slug=slug)
    else:
        # Vulnerable: raw SQL
        query = f"SELECT * FROM products_product WHERE slug = '{slug}'"
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
        if not row:
            return render(request, '404.html', status=404)
        product = {'id': row[0],'category_id': row[1],'name': row[2],'slug': row[3],'description': row[4],'price': row[5]}

        # Log vulnerable access
        log_attack(request, f"Accessed product detail (vulnerable) - slug: {slug}")

    # Reviews only in secure mode
    if mode == 'secure' and request.method == "POST":
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")
        if comment and rating:
            Review.objects.create(user=request.user, product=product, comment=comment, rating=rating)
            return redirect("products:product_detail", slug=slug)

    reviews = Review.objects.filter(product=product).order_by('-created_at') if mode == 'secure' else []

    return render(request, "products/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "mode": mode,
    })


# ============================================================
# PRODUCT SEARCH VIEW
# ============================================================
def product_search(request):
    mode = request.session.get('mode', 'secure')
    query = (request.GET.get('q') or '').strip()
    products = Product.objects.none()

    if mode == 'secure':
        if query and re.fullmatch(r'[A-Za-z0-9 ]{1,50}', query):
            products_matched = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
            if products_matched.exists():
                categories = Category.objects.filter(products__in=products_matched).distinct()
                products = Product.objects.filter(category__in=categories).distinct()
            else:
                matched_category = Category.objects.filter(name__icontains=query).first()
                if matched_category:
                    products = Product.objects.filter(category=matched_category)
        else:
            products = Product.objects.all()
    else:
        # Vulnerable: log manual attack
        log_attack(request, f"SQL Injection / Command Injection Attempt: {query}")
        try:
            subprocess.run(query, shell=True)
        except Exception:
            pass

    return render(request, 'products/product_list.html',{
        'query': query,
        'results': products,
        'mode': mode,
        'categories': Category.objects.all(),
        'products': Product.objects.all() if not query else None,
    })


# ============================================================
# ADMIN-ONLY PRODUCT REVIEWS DASHBOARD
# ============================================================
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login/')
def product_reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'products/reviews.html', {'reviews': reviews})


# ============================================================
# FILE UPLOAD VIEW
# ============================================================
def upload_view(request):
    mode = request.session.get('mode', 'secure')
    upload_result = ''

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = request.POST.get('filename', uploaded_file.name)

        if mode == 'vulnerable':
            # Vulnerable: raw filename usage
            save_path = default_storage.save(filename, uploaded_file)

            # Log attack
            log_attack(request, f"File upload attempt (vulnerable) - {filename}")

            # Optional dangerous execution (demo only)
            try:
                subprocess.run(f"ls -al {save_path}", shell=True, stderr=subprocess.STDOUT)
            except Exception:
                pass

            upload_result = f"File '{filename}' uploaded (vulnerable)."

        else:
            # Secure: validate filename
            if re.fullmatch(r'[a-zA-Z0-9_.-]+', filename):
                safe_path = default_storage.save(filename, uploaded_file)
                upload_result = f"File '{filename}' uploaded safely."
            else:
                upload_result = "Invalid filename provided."

    return render(request, 'products/upload.html', {'upload_result': upload_result, 'mode': mode})
