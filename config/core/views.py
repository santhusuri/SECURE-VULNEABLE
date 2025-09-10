from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage



import subprocess
import re
import threading
import os


# ======================================================
# MODE TOGGLING (Secure / Vulnerable)
# ======================================================
def toggle_mode_page(request):
    """
    Toggle between 'secure' and 'vulnerable' simulation modes.
    - Stores current mode in session.
    - Redirects user back to the referring page (or product list as fallback).
    """
    current = request.session.get('mode', 'secure')
    request.session['mode'] = 'vulnerable' if current == 'secure' else 'secure'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('products:product_list')))

def toggle_mode_api(request):
    """
    Toggle mode via AJAX (for JS toggle button).
    """
    if request.method == "POST":
        mode = request.POST.get('mode')
        request.session['mode'] = mode
        return JsonResponse({"status": "ok", "mode": mode})
    return JsonResponse({"status": "failed"}, status=400)


# ======================================================
# COMMAND INJECTION DEMO (Search View)
# ======================================================
def search_view(request):
    """
    Demonstrates command injection vulnerability in 'vulnerable' mode.
    """
    mode = request.session.get('mode', 'secure')
    search_result = ''

    if request.method == 'POST':
        query = request.POST.get('query', '')

        if mode == 'vulnerable':
            try:
                # Vulnerable: raw input passed to shell
                result = subprocess.check_output(
                    f"ping -c 1 {query}",
                    shell=True, stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                search_result = result
            except subprocess.CalledProcessError as e:
                search_result = e.output
        else:
            # Secure: validate input + safe execution
            if re.fullmatch(r'[a-zA-Z0-9\.\-]+', query):
                try:
                    result = subprocess.check_output(
                        ['ping', '-c', '1', query],
                        universal_newlines=True
                    )
                    search_result = result
                except subprocess.CalledProcessError as e:
                    search_result = e.output
            else:
                messages.error(request, "Invalid input provided.")

    return render(request, 'search.html', {'search_result': search_result})


# ======================================================
# FILE UPLOAD DEMO (Path / Command Injection)
# ======================================================
def upload_view(request):
    """
    Demonstrates file upload handling vulnerability.
    """
    mode = request.session.get('mode', 'secure')
    upload_result = ''

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = request.POST.get('filename', uploaded_file.name)

        if mode == 'vulnerable':
            # Vulnerable: raw filename usage
            save_path = default_storage.save(filename, uploaded_file)
            try:
                result = subprocess.check_output(
                    f"ls -al {save_path}",
                    shell=True, stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                upload_result = result
            except subprocess.CalledProcessError as e:
                upload_result = e.output
        else:
            # Secure: validate filename
            if re.fullmatch(r'[a-zA-Z0-9_.-]+', filename):
                safe_path = default_storage.save(filename, uploaded_file)
                try:
                    result = subprocess.check_output(
                        ['ls', '-al', safe_path],
                        universal_newlines=True
                    )
                    upload_result = result
                except subprocess.CalledProcessError as e:
                    upload_result = e.output
            else:
                messages.error(request, "Invalid filename provided.")

    return render(request, 'upload.html', {'upload_result': upload_result})


from django.shortcuts import render
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ids_dashboard(request):
    IDS_LOG_FILE = os.path.join(BASE_DIR, "ids_dashboard/ids.log")
    if os.path.exists(IDS_LOG_FILE):
        with open(IDS_LOG_FILE) as f:
            logs = f.readlines()
    else:
        logs = ["No logs yet."]
    return render(request, "ids_dashboard/ids_dashboard.html", {"logs": logs})

def airs_dashboard(request):
    AIRS_LOG_FILE = os.path.join(BASE_DIR, "airs_dashboard/airs.log")
    if os.path.exists(AIRS_LOG_FILE):
        with open(AIRS_LOG_FILE) as f:
            logs = f.readlines()
    else:
        logs = ["No logs yet."]
    return render(request, "airs_dashboard/airs_dashboard.html", {"logs": logs})
