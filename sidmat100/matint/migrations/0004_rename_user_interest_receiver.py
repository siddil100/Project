# Generated by Django 4.2.7 on 2023-11-22 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matint', '0003_interest_sender_alter_interest_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interest',
            old_name='user',
            new_name='receiver',
        ),
    ]