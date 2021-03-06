# Generated by Django 2.2.28 on 2022-06-07 02:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("katadzuke_app_v1", "0004_auto_20220607_1110"),
    ]

    operations = [
        migrations.AlterField(
            model_name="roomphoto",
            name="percent_of_floors",
            field=models.IntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
    ]
