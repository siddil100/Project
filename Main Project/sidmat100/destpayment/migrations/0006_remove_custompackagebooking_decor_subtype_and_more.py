# Generated by Django 4.2.7 on 2024-03-28 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('destpayment', '0005_custompackagebooking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custompackagebooking',
            name='decor_subtype',
        ),
        migrations.RemoveField(
            model_name='custompackagebooking',
            name='event_subtype',
        ),
        migrations.RemoveField(
            model_name='custompackagebooking',
            name='food_subtype',
        ),
    ]
