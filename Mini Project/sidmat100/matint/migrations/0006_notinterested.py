# Generated by Django 4.2.7 on 2023-11-26 02:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0037_blockeduser_blocked_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matint', '0005_interestedprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotInterested',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_interested_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='not_interested_by', to=settings.AUTH_USER_MODEL)),
                ('not_interested_user_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matrimony.personaldetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='not_interested_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]