# accounts/migrations/0002_create_lab_users.py
from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_lab_users(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    VulnUser = apps.get_model('accounts', 'VulnUser')

    # --- Secure user ---
    if not User.objects.filter(username='secure_user').exists():
        User.objects.create(
            username='secure_user',
            email='secure@example.com',
            password=make_password('securepass123')  # hashed password
        )

    # --- Vulnerable users (plain text) ---
    vuln_users = [
        {"username": "vuln1", "password": "pass1"},
        {"username": "vuln2", "password": "pass2"},
        {"username": "vuln3", "password": "pass3"},
        {"username": "vuln4", "password": "pass4"},
        {"username": "vuln5", "password": "pass5"},
    ]

    for vu in vuln_users:
        if not VulnUser.objects.filter(username=vu['username']).exists():
            VulnUser.objects.create(
                username=vu['username'],
                password=vu['password']  # plain text
            )

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # replace with your previous migration
    ]

    operations = [
        migrations.RunPython(create_lab_users),
    ]
