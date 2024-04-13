from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FoodOption)
admin.site.register(DecorationOption)
admin.site.register(EventOption)
admin.site.register(License)
admin.site.register(Scheduling)
admin.site.register(SchedulingBooking)

