# Generated by Django 4.2.7 on 2023-11-22 00:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('matint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='interest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
