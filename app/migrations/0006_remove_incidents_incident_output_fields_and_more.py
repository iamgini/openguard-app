# Generated by Django 4.0.2 on 2022-03-03 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_incidents_incident_output_fields_new_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidents',
            name='incident_output_fields',
        ),
        migrations.RemoveField(
            model_name='incidents',
            name='incident_output_fields_new',
        ),
    ]