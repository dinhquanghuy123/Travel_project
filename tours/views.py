from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Tour, Review
from django.contrib.auth.decorators import login_required


def home_view(request):
    tours = Tour.objects.all()

    keyword = request.GET.get('q')

    if keyword:
        tours = tours.filter(
            Q(name__icontains=keyword) |
            Q(destination__icontains=keyword)
        )

    destination = request.GET.get('destination')

    if destination:
        tours = tours.filter(destination=destination)
    sort = request.GET.get('sort')

    if sort == 'low':
        tours = tours.order_by('price')
    elif sort == 'high':
        tours = tours.order_by('-price')

    return render(request, 'tours/home.html', {
        'tours': tours
    })


def tour_detail_view(request, id):
    tour = get_object_or_404(Tour, id=id)
    reviews = Review.objects.filter(tour=tour)

    return render(request, 'tours/detail.html', {
        'tour': tour,
        'reviews': reviews
    })


@login_required
def add_review_view(request, id):
    tour = get_object_or_404(Tour, id=id)

    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']

        Review.objects.create(
            user=request.user,
            tour=tour,
            rating=rating,
            comment=comment
        )

        return redirect('tour_detail', id=tour.id)
