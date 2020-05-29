# Generated by Django 3.0.6 on 2020-05-20 17:15

from django.db import migrations, models


# pylint: disable=all
# generated by django

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaptchaSubmissions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('x_coord', models.IntegerField()),
                ('y_coord', models.IntegerField()),
                ('year', models.IntegerField()),
                ('water', models.BooleanField()),
                ('land', models.BooleanField()),
                ('buildings', models.BooleanField()),
                ('church', models.BooleanField()),
                ('oiltank', models.BooleanField()),
            ],
        ),
    ]
