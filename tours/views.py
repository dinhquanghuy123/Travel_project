from django.shortcuts import render, get_object_or_404
from .models import Tour, Review


def home_view(request):
    tours = Tour.objects.all()
    return render(request, 'tours/home.html', {'tours': tours})


def tour_detail_view(request, id):
    tour = get_object_or_404(Tour, id=id)
    reviews = Review.objects.filter(tour=tour)

    return render(request, 'tours/detail.html', {
        'tour': tour,
        'reviews': reviews
    })
