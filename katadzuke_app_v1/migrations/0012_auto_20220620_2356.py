# Generated by Django 2.2.28 on 2022-06-20 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('katadzuke_app_v1', '0011_auto_20220619_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='full_score_photo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='katadzuke_app_v1.RoomPhoto'),
        ),
    ]
