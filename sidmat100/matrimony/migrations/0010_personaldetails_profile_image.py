# Generated by Django 4.2.7 on 2023-11-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0009_alter_personaldetails_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetails',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
