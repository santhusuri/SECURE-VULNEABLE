# Secure vs Vulnerable Web Application with Real-Time IDS & AIRS Logging

## Project Overview
This project is an interactive web application designed for **cybersecurity training and demonstration purposes**. It features two modes:

- **Secure Mode**: Implements best practices with Django ORM, hashed passwords, and input validation.
- **Vulnerable Mode**: Intentionally introduces common web vulnerabilities, including SQL Injection, Command Injection, and unsafe file uploads.

The application includes **real-time attack monitoring dashboards**:

- **IDS Dashboard**: Detects and logs suspicious activities such as SQL Injection attempts.
- **AIRS Dashboard**: Provides alerts for potential unauthorized access, malware, or suspicious user actions.

All attacks performed in **vulnerable mode**, including manual testing from login forms, search, product details, or file uploads, are automatically logged in **IDS** and **AIRS dashboards**. This allows admins to observe attacks in real-time.

---

## Features

### Vulnerable Mode
- SQL Injection vulnerability in login form and product search.
- Command injection vulnerability in product search and file uploads.
- Direct file uploads without sanitization.
- Manual attacks automatically logged to IDS & AIRS.

### Secure Mode
- Django ORM-based queries to prevent SQL Injection.
- Hashed passwords for user accounts.
- Validated file uploads and sanitized inputs.

### Dashboards
- **IDS**: Displays detailed logs of suspicious activities.
- **AIRS**: Shows high-level alerts of potential security threats.
- Logs update in real-time with AJAX polling.

---

## Tech Stack
- **Backend**: Django 5.2.6, Python 3.12
- **Database**: SQLite (default for demo; easily replaceable with PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5 (optional), HTML, JavaScript
- **Real-Time Logging**: AJAX-based log polling for IDS & AIRS dashboards

---

## Project Structure


---

## Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/santhusuri/SECURE-VULNERABLE.git
    cd SECURE-VULNERABLE/config

2. **Create and activate virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Apply migrations**
    ```bash
    python manage.py migrate

5. **Create superuser**
    ```bash
    python manage.py createsuperuser

6. **Run the Django development server**
    ```bash
    python manage.py runserver

7.**Access the application**
- Open your browser at http://127.0.0.1:8000/

- Toggle between secure and vulnerable mode via /toggle_mode/ or UI toggle button.

- Access dashboards:

    - IDS: http://127.0.0.1:8000/ids_dashboard/

    - AIRS: http://127.0.0.1:8000/airs_dashboard/

---

## How to Test Attacks

1. **Login Form SQL Injection**

- Switch to vulnerable mode

- Enter admin' OR '1'='1 as username or password

- Observe IDS & AIRS dashboards for the log

2. **Product Search Command Injection**

- Switch to vulnerable mode

- Enter shell commands (e.g., ls) in the search bar

- Logs will appear in IDS & AIRS

3. **File Upload**

- Upload any file in vulnerable mode

- The upload attempt will be logged

All attacks, even from guest sessions or remote machines (e.g., via ngrok tunnel), are captured in real-time in the dashboards.

---

## Security Notes

- The vulnerable mode is strictly for training and demonstration purposes.

- Do not deploy vulnerable mode to production.

- IDS & AIRS logging demonstrates real-time attack detection and is for educational use.