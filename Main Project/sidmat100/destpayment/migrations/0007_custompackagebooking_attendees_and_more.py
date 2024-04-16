# Generated by Django 4.2.7 on 2024-03-30 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destpayment', '0006_remove_custompackagebooking_decor_subtype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompackagebooking',
            name='attendees',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='custompackagebooking',
            name='location',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]