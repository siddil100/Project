from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *



admin.site.register(Interest)
admin.site.register(InterestedProfile)
admin.site.register(NotInterested)
admin.site.register(UserActivity)
