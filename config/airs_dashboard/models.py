from django.db import models

class AIRSAlert(models.Model):
    alert_id = models.CharField(max_length=50)
    alert_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.alert_id} - {self.alert_type}"
