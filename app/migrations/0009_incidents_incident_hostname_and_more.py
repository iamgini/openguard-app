# Generated by Django 4.0.2 on 2022-03-04 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_incidents_incident_rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidents',
            name='incident_hostname',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='incidents',
            name='incident_output',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='incidents',
            name='incident_rule',
            field=models.CharField(default='', max_length=300),
        ),
    ]
