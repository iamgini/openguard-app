# Generated by Django 4.0.2 on 2022-03-03 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_incidents_incident_output_fields_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidents',
            name='incident_output',
            field=models.CharField(default='', max_length=1000),
        ),
    ]