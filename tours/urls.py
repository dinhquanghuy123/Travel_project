from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tour/<int:id>/', views.tour_detail_view, name='tour_detail'),
    path('tour/<int:id>/review/', views.add_review_view, name='add_review'),
]
