# Generated by Django 4.2 on 2024-05-26 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_userpayment_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpayment',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]