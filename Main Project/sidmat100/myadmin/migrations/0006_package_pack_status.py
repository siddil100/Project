# Generated by Django 4.2.7 on 2024-04-04 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0005_package_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='pack_status',
            field=models.BooleanField(default=True),
        ),
    ]
