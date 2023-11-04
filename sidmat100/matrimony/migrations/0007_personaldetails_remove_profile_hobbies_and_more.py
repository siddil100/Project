# Generated by Django 4.2.7 on 2023-11-04 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrimony', '0006_remove_profile_caste_delete_caste'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('middle_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(max_length=15)),
                ('mother_tongue', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='hobbies',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='religion',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sect',
        ),
        migrations.RemoveField(
            model_name='sect',
            name='religion',
        ),
        migrations.DeleteModel(
            name='hobby',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Religion',
        ),
        migrations.DeleteModel(
            name='Sect',
        ),
    ]