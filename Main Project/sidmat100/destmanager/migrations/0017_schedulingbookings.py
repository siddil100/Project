# Generated by Django 4.2.7 on 2024-04-07 03:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('destmanager', '0016_scheduling_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchedulingBookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('booking_count', models.IntegerField()),
                ('limit', models.IntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
