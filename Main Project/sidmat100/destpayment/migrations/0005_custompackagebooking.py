# Generated by Django 4.2.7 on 2024-03-28 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('destpayment', '0004_packagebooking_event_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPackageBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_date', models.DateTimeField(blank=True, null=True)),
                ('event_date', models.DateTimeField(blank=True, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('package_name', models.CharField(max_length=255)),
                ('decor_type', models.CharField(max_length=255)),
                ('decor_subtype', models.CharField(max_length=255)),
                ('event_type', models.CharField(max_length=255)),
                ('event_subtype', models.CharField(max_length=255)),
                ('food_type', models.CharField(max_length=255)),
                ('food_subtype', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
