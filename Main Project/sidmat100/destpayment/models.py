from django.db import models
from myadmin.models import Package
from django.contrib.auth.models import User
# Create your models here.


class PackageBooking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.package.package_name}'