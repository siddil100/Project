# Generated by Django 4.2.7 on 2023-11-04 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0008_personaldetails_first_name_personaldetails_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldetails',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
