# Generated by Django 4.2.7 on 2024-04-06 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destmanager', '0014_rename_events_eventoption_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('booking_count', models.IntegerField()),
                ('limit', models.IntegerField()),
            ],
        ),
    ]
