from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tours.models import Tour
from .models import Booking


@login_required
def create_booking_view(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])

        if quantity > tour.slots:
            return render(request, 'bookings/create.html', {
                'tour': tour,
                'error': 'Không đủ chỗ trống'
            })

        total_price = quantity * tour.price

        Booking.objects.create(
            user=request.user,
            tour=tour,
            quantity=quantity,
            total_price=total_price
        )

        tour.slots -= quantity
        tour.save()

        return redirect('booking_history')

    return render(request, 'bookings/create.html', {
        'tour': tour
    })


@login_required
def booking_history_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')

    return render(request, 'bookings/history.html', {
        'bookings': bookings
    })
