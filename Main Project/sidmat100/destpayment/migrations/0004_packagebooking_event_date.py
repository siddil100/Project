# Generated by Django 4.2.7 on 2024-03-27 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destpayment', '0003_packagebooking_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagebooking',
            name='event_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]