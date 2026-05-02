from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Tour, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator


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
        tours = tours.filter(destination__iexact=destination)
    sort = request.GET.get('sort', '').strip()

    if sort == 'low':
        tours = tours.order_by('price')
    elif sort == 'high':
        tours = tours.order_by('-price')
    else:
        tours = tours.order_by('-created_at')

    # 🔥 PAGINATION
    paginator = Paginator(tours, 6)  # 6 tour / page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(request, 'tours/home.html', {
        'tours': page_obj,
        'query_params': query_params.urlencode()
    })


def tour_detail_view(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = Review.objects.filter(tour=tour)\
        .select_related('user')\
        .order_by('-created_at')

    return render(request, 'tours/detail.html', {
        'tour': tour,
        'reviews': reviews
    })


@login_required
def add_review_view(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    if request.method == 'POST':

        try:
            rating = int(request.POST.get('rating', 5))
        except ValueError:
            messages.error(request, 'Số sao không hợp lệ.')
            return redirect('tour_detail', pk=tour.id)

        comment = request.POST.get('comment', '').strip()

        # Validate rating
        if rating < 1 or rating > 5:
            messages.error(request, 'Số sao không hợp lệ.')
            return redirect('tour_detail', pk=tour.id)

        # Kiểm tra đã review chưa
        if Review.objects.filter(
            user=request.user,
            tour=tour
        ).exists():

            messages.warning(
                request,
                'Bạn đã đánh giá tour này rồi.'
            )

            return redirect('tour_detail', pk=tour.id)

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

    return redirect('tour_detail', pk=tour.id)
