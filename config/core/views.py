from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

import subprocess
import re
import os
from django.core.files.storage import default_storage


# ======================================================
# MODE TOGGLING (Secure / Vulnerable)
# ======================================================
def toggle_mode(request):
    """
    Toggle between 'secure' and 'vulnerable' simulation modes.
    - Stores current mode in session.
    - Redirects user back to the referring page (or product list as fallback).
    """
    current = request.session.get('sim_mode', 'secure')
    request.session['sim_mode'] = 'vulnerable' if current == 'secure' else 'secure'

    # Redirect back to where the user came from, or fallback to product_list
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('product_list')))


# ======================================================
# COMMAND INJECTION DEMO (Search View)
# ======================================================
def search_view(request):
    """
    Demonstrates command injection vulnerability in 'vulnerable' mode.
    - Vulnerable Mode:
        Directly executes shell command with user input (ping).
    - Secure Mode:
        Validates input against regex whitelist (hostnames/IPs).
        Executes command safely using list arguments.
    """
    mode = request.session.get('mode', 'secure')
    search_result = ''

    if request.method == 'POST':
        query = request.POST.get('query', '')

        if mode == 'vulnerable':
            # -----------------------------
            # Vulnerable: Direct raw input to shell
            # -----------------------------
            try:
                result = subprocess.check_output(
                    f"ping -c 1 {query}",
                    shell=True, stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                search_result = result
            except subprocess.CalledProcessError as e:
                search_result = e.output

        else:
            # -----------------------------
            # Secure: Validate input + safe execution
            # -----------------------------
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
    Demonstrates file upload handling.
    - Vulnerable Mode:
        Uses raw filename directly in OS command (possible injection).
    - Secure Mode:
        Validates filename with regex whitelist before saving.
        Uses safe subprocess execution (list args).
    """
    mode = request.session.get('mode', 'secure')
    upload_result = ''

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = request.POST.get('filename', uploaded_file.name)

        if mode == 'vulnerable':
            # -----------------------------
            # Vulnerable: Direct filename usage
            # -----------------------------
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
            # -----------------------------
            # Secure: Validate filename
            # -----------------------------
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
