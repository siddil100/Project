# Generated by Django 4.2.7 on 2023-11-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0007_personaldetails_remove_profile_hobbies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetails',
            name='first_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='last_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
