# Generated by Django 4.2.7 on 2023-12-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matpayment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='premiummembership',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]