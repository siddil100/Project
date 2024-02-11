# Generated by Django 4.2.7 on 2023-11-05 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrimony', '0013_personaldetails_marital_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('number_of_siblings', models.PositiveIntegerField()),
                ('father_occupation', models.CharField(max_length=100)),
                ('mother_occupation', models.CharField(max_length=100)),
                ('family_type', models.CharField(max_length=100)),
                ('family_status', models.CharField(max_length=100)),
                ('number_of_family_members', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]