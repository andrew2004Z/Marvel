from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, '../templates/base.html')


def popular_comics(request):
    return render(request, '../templates/popular_comics.html')