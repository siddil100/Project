# Generated by Django 4.2.7 on 2023-11-12 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0030_locationdetails_email_verification_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetails',
            name='aadhar_valid',
            field=models.BooleanField(default=True),
        ),
    ]
