# Generated by Django 4.0.2 on 2022-03-03 11:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Incidents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_time', models.DateTimeField(auto_now=True)),
                ('incident_priority', models.CharField(default='', max_length=10)),
                ('incident_rule', models.CharField(default='', max_length=25)),
                ('incident_output', models.CharField(default='', max_length=100)),
                ('incident_output_fields', models.CharField(default='', max_length=1000)),
            ],
        ),
    ]
