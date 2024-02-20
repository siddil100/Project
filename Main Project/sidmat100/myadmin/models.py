from django.db import models

# Create your models here.


from django.db import models

class Package(models.Model):
    package_name = models.CharField(max_length=100)
    star_rating = models.IntegerField()
    meal_preference = models.CharField(max_length=50)
    attendees = models.IntegerField()
    days_count = models.IntegerField()
    program_count = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='package_images/')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.package_name
