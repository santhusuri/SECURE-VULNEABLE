from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from core.logger import write_ids_log, write_airs_log
from .forms import RegistrationForm, LoginForm
from .models import VulnUser  # Vulnerable user model for SQLi demo

# ======================================================
# ACCOUNTS APP VIEWS
# ======================================================

User = get_user_model()  # Use Django’s custom User model if overridden


# ======================================================
# User Registration
# ======================================================
def register_view(request):
    """
    Handles user registration.
    - Vulnerable mode:
        Stores password in plain text (for training/demo labs only).
    - Secure mode:
        Uses Django's form validation + hashed password storage.
    """
    if request.session.get('mode') == 'vulnerable' and settings.VULNERABLE_LABS.get('weak_password_hash'):
        # -----------------------------
        # Vulnerable Registration Path
        # -----------------------------
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')  # Collected but unused
            VulnUser.objects.create(username=username, password=password)
            messages.warning(request, "Registered with WEAK password storage (vulnerable mode).")
            return redirect('accounts:login')
        return render(request, 'accounts/vuln_register.html')

    # -----------------------------
    # Secure Registration Path
    # -----------------------------
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Automatically hashes password
            messages.success(request, "Registration successful. Please log in.")
            return redirect('accounts:login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# ======================================================
# User Login
# ======================================================
from core.logger import write_ids_log, write_airs_log

def login_view(request):
    """
    Handles user login.
    - Vulnerable mode:
        Uses raw SQL query (intentionally SQL injection prone).
        Logs all login attempts to IDS/AIRS.
    - Secure mode:
        Uses Django’s built-in authentication.
    """
    mode = request.session.get('mode') or ('secure' if getattr(settings, 'SECURE_MODE', True) else 'vulnerable')

    if mode == 'vulnerable':
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Log all login attempts
            user_id = username or "guest"
            write_ids_log(user_id, f"Login attempt on vulnerable login page - username: {username}")
            write_airs_log("unauthorized_access")

            # INTENTIONALLY VULNERABLE: raw SQL
            query = f"SELECT id FROM accounts_vulnuser WHERE username='{username}' AND password='{password}'"
            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()

            if row:
                try:
                    secure_user = User.objects.get(username="secure_user")
                    login(request, secure_user)
                    messages.warning(request, "Logged in via Vulnerable Mode (SQLi bypass).")

                    # Log successful bypass
                    write_ids_log(user_id, "Successful login via vulnerable SQLi bypass")
                    write_airs_log("unauthorized_access")

                    return redirect('accounts:profile')
                except User.DoesNotExist:
                    messages.error(request, "Secure user not found. Cannot complete login.")
            else:
                messages.error(request, "Invalid credentials (or SQLi failed).")
                # Log failed login attempt
                write_ids_log(user_id, "Failed login attempt on vulnerable login page")
                write_airs_log("unauthorized_access")

        return render(request, 'accounts/vuln_login.html')

    else:
        # Secure mode
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('accounts:profile')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

# ======================================================
# User Logout
# ======================================================
def logout_view(request):
    """
    Logs out the current user and redirects to home.
    """
    logout(request)
    return redirect('home')


# ======================================================
# User Profile
# ======================================================
def profile_view(request):
    """
    Displays the current user's profile page.
    """
    return render(request, 'accounts/profile.html')


# ======================================================
# Secure/Vulnerable Mode Toggle
# ======================================================


@csrf_exempt  # ✅ Not strictly needed if CSRF token is sent (JS does send it)
def toggle_mode(request):
    """
    Toggle between Secure Mode and Vulnerable Mode.

    Session key: `request.session['mode']`
        - "secure" (default)
        - "vulnerable"

    Returns:
        JsonResponse: { "mode": "secure" or "vulnerable" }
    """
    mode = request.session.get("mode", "secure")
    if mode == "secure":
        request.session["mode"] = "vulnerable"
    else:
        request.session["mode"] = "secure"

    return JsonResponse({"mode": request.session["mode"]})

