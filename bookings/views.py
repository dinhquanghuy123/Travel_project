from django.shortcuts import render
from django.http import HttpResponse


def create_booking_view(request, tour_id):
    return HttpResponse(f"Booking tour {tour_id}")


def booking_history_view(request):
    return HttpResponse("Booking history")
