# Generated by Django 4.2.7 on 2024-02-19 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=100)),
                ('star_rating', models.IntegerField()),
                ('meal_preference', models.CharField(max_length=50)),
                ('attendees', models.IntegerField()),
                ('days_count', models.IntegerField()),
                ('program_count', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='package_images/')),
            ],
        ),
    ]
