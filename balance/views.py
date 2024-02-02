# myapp/views.py
from django.shortcuts import render


def index(request):
    context = {'name': 'Hordii'}  # Replace 'Your Name' with the desired value
    return render(request, 'index.html', context)
