import json
from django.core.management.base import BaseCommand
from airs_dashboard.models import AIRSAlert

class Command(BaseCommand):
    help = 'Read suricata alerts and store in database'

    def handle(self, *args, **kwargs):
        with open('suricata/alerts.json') as f:
            data = json.load(f)
            for alert in data:
                AIRSAlert.objects.create(
                    alert_id = alert['alert_id'],
                    alert_type = alert['alert_type']
                )
        self.stdout.write(self.style.SUCCESS('Suricata alerts updated!'))
