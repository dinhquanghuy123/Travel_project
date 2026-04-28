from django.db import models
from django.contrib.auth.models import User


class Tour(models.Model):
    name = models.CharField(max_length=200)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Số ngày")
    slots = models.PositiveIntegerField(default=10)
    description = models.TextField()
    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.name} ({self.rating})"


class Meta:
    unique_together = ('user', 'tour')
