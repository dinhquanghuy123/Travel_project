from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:tour_id>/', views.create_booking_view, name='create_booking'),
    path('history/', views.booking_history_view, name='booking_history'),
    path('cancel/<int:booking_id>/',
         views.cancel_booking_view, name='cancel_booking'),
    path('confirm/<int:booking_id>/',
         views.confirm_booking_view, name='confirm_booking'),
]
