# Generated by Django 4.2.7 on 2024-03-21 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('destmanager', '0013_eventoption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventoption',
            old_name='events',
            new_name='event',
        ),
    ]
