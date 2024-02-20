from django.shortcuts import render

# matdest/views.py

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required



@never_cache
@login_required(login_url='accounts:login')
def desthome(request):
    return render(request, 'matdest/desthome.html')



from django.shortcuts import render
from myadmin.models import Package


@never_cache
@login_required(login_url='accounts:login')
def view_packages(request):
    packages = Package.objects.all()
    return render(request, 'matdest/view_packages.html', {'packages': packages})
