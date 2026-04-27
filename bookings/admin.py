from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour',
                    'quantity', 'total_price', 'status', 'booked_at')
    search_fields = ('user__username', 'tour__name')
    list_filter = ('status',)
