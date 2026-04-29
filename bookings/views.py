from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from tours.models import Tour
from .models import Booking


@login_required
def create_booking_view(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':

        quantity = int(request.POST.get('quantity', 1))

        # Validate
        if quantity <= 0:
            messages.error(request, 'Số lượng không hợp lệ.')
            return redirect('create_booking', tour_id=tour.id)

        if quantity > tour.slots:
            return render(request, 'bookings/create.html', {
                'tour': tour,
                'error': 'Không đủ chỗ trống.'
            })

        # Tạo booking
        booking = Booking.objects.create(
            user=request.user,
            tour=tour,
            quantity=quantity
        )

        # Trừ slot
        tour.slots -= quantity
        tour.save()

        messages.success(request, 'Đặt tour thành công!')

        return redirect('booking_history')

    return render(request, 'bookings/create.html', {
        'tour': tour
    })


@login_required
def booking_history_view(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('tour')

    return render(request, 'bookings/history.html', {
        'bookings': bookings
    })
