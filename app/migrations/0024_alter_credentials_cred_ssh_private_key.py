# Generated by Django 4.0.3 on 2022-03-17 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_incidents_incident_report_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentials',
            name='cred_ssh_private_key',
            field=models.TextField(default=' ', max_length=5000),
        ),
    ]
