# Generated by Django 4.0.2 on 2022-03-03 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_credentials_managednodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidents',
            name='incident_time_reported',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='incidents',
            name='incident_time',
            field=models.DateTimeField(),
        ),
    ]
