# Generated by Django 2.2.28 on 2022-06-19 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("katadzuke_app_v1", "0010_user_full_score_photo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="full_score_photo_public_id",
        ),
        migrations.RemoveField(
            model_name="user",
            name="full_score_photo_url",
        ),
        migrations.RemoveField(
            model_name="user",
            name="full_score_room_percent_of_floors",
        ),
        migrations.AlterField(
            model_name="user",
            name="full_score_photo",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="katadzuke_app_v1.RoomPhoto",
            ),
        ),
    ]
