from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    return HttpResponse("Home page")


def tour_detail_view(request, id):
    return HttpResponse(f"Tour {id}")
