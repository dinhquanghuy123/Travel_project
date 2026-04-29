from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Tour, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home_view(request):
    tours = Tour.objects.all()

    keyword = request.GET.get('q', '').strip()

    if keyword:
        tours = tours.filter(
            Q(name__icontains=keyword) |
            Q(destination__icontains=keyword)
        )

    destination = request.GET.get('destination', '').strip()

    if destination:
        tours = tours.filter(destination=destination)
    sort = request.GET.get('sort', '').strip()

    if sort == 'low':
        tours = tours.order_by('price')
    elif sort == 'high':
        tours = tours.order_by('-price')
    else:
        tours = tours.order_by('-created_at')

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

        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()

        # Validate rating
        if rating < 1 or rating > 5:
            messages.error(request, 'Số sao không hợp lệ.')
            return redirect('tour_detail', id=tour.id)

        # Kiểm tra đã review chưa
        if Review.objects.filter(
            user=request.user,
            tour=tour
        ).exists():

            messages.warning(
                request,
                'Bạn đã đánh giá tour này rồi.'
            )

            return redirect('tour_detail', id=tour.id)

        Review.objects.create(
            user=request.user,
            tour=tour,
            rating=rating,
            comment=comment
        )

        messages.success(
            request,
            'Gửi đánh giá thành công!'
        )

    return redirect('tour_detail', id=tour.id)
