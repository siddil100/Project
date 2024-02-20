# Generated by Django 4.2.7 on 2024-02-20 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myadmin', '0002_package_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_date', models.DateTimeField(blank=True, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.package')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
