# Generated by Django 4.2.7 on 2024-04-04 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0004_package_dectype_package_subcategory_package_subtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='description',
            field=models.TextField(default='No description provided'),
        ),
    ]
