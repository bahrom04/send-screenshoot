# Generated by Django 4.2 on 2024-07-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0014_alter_plan_options_alter_userpayment_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="description",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
