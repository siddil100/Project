from django.shortcuts import render

# matdest/views.py

from django.shortcuts import render

def desthome(request):
    return render(request, 'matdest/desthome.html')
