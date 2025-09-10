# core/apps.py
from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)
        open(os.path.join(BASE_DIR, "logs/ids.log"), 'a').close()
        open(os.path.join(BASE_DIR, "logs/airs.log"), 'a').close()
