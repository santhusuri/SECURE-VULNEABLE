# Secure-Vulnerable E-Commerce Web Application 🛒

A **dummy e-commerce web application** designed for **web application penetration testing practice**.  
This project allows users to **toggle between secure and vulnerable modes** to test and learn about common web vulnerabilities in a controlled environment.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Security Modes](#security-modes)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- Toggle between **vulnerable** and **secure** modes.
- Vulnerable mode includes common web vulnerabilities for learning:
  - SQL Injection (SQLi)
  - Cross-Site Scripting (XSS)
  - Cross-Site Request Forgery (CSRF)
  - Insecure authentication & session management
- Secure mode implements mitigations for all vulnerabilities.
- Dummy e-commerce functionality: product catalog, cart, checkout, and user login.
- Easy to deploy locally or via **ngrok** for external access.

---


---

## Getting Started

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (optional but recommended)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/santhusuri/SECURE-VULNEABLE.git
    cd SECURE-VULNEABLE

2. Create a virtual environment:
    python -m venv venv
    source venv/bin/activate       # Linux/macOS
    venv\Scripts\activate          # Windows

3. Install dependencies:
    pip install -r requirements.txt


## Usage

### Run the application:

1. RUN THE SERVER 
  
  python manage.py runserver 8000

2. Using ngrok (optional) Expose the local app to the internet:

ngrok http 8000  # For Django