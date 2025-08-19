from django.db import models

class Shipment(models.Model):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='shipment')
    tracking_number = models.CharField(max_length=100)
    carrier = models.CharField(max_length=100)
    estimated_delivery = models.DateField()
    shipped_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('shipped', 'Shipped'),
            ('in_transit', 'In Transit'),
            ('delivered', 'Delivered'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"Shipment for Order #{self.order.id} - {self.status}"
