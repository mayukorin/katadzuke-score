# Generated by Django 2.2.28 on 2022-06-19 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('katadzuke_app_v1', '0009_auto_20220612_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_score_photo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='katadzuke_app_v1.RoomPhoto'),
        ),
    ]
