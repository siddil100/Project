# Generated by Django 4.2.7 on 2023-12-02 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]