# Generated by Django 4.2.7 on 2024-03-14 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destmanager', '0005_alter_license_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='dob',
            field=models.DateField(),
        ),
    ]