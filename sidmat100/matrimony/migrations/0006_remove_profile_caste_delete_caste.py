# Generated by Django 4.2.3 on 2023-09-24 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0005_remove_profile_father_delete_fatherprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='caste',
        ),
        migrations.DeleteModel(
            name='Caste',
        ),
    ]
