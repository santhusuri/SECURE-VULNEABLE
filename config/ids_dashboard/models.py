from django.db import models

class ActionLog(models.Model):
    user_id = models.IntegerField()
    action_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_id} - {self.action_type}"
