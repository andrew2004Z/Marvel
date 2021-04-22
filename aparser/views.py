from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    data = popular()
    return render(request, '../templates/base.html')
