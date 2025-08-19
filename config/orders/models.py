from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add any other fields you need, e.g., status, shipping address, etc.

    def __str__(self):
        return f"Order #{self.id} by {self.user or 'Guest'} - Total: ${self.total}"
