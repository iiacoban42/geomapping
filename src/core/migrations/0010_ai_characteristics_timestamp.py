# Generated by Django 3.0.6 on 2020-06-14 05:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200612_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='ai_characteristics',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]