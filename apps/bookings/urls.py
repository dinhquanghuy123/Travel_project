from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:pk>/', views.create_booking_view, name='create_booking'),
    path('history/', views.booking_history_view, name='booking_history'),
    path('cancel/<int:pk>/',
         views.cancel_booking_view, name='cancel_booking'),
    path('confirm/<int:pk>/',
         views.confirm_booking_view, name='confirm_booking'),
]
