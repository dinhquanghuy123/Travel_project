from django.db import models
from django.contrib.auth.models import User
from tours.models import Tour


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('cancelled', 'Đã hủy'),
        ('completed', 'Hoàn thành'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.tour.price
        super().save(*args, **kwargs)
