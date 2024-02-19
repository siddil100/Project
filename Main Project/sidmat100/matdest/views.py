from django.shortcuts import render

# matdest/views.py

from django.shortcuts import render

def desthome(request):
    return render(request, 'matdest/desthome.html')



from django.shortcuts import render
from myadmin.models import Package

def view_packages(request):
    packages = Package.objects.all()
    return render(request, 'matdest/view_packages.html', {'packages': packages})
