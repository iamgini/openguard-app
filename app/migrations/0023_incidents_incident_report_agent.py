# Generated by Django 4.0.3 on 2022-03-10 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_managednodes_instance_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidents',
            name='incident_report_agent',
            field=models.CharField(default='', max_length=50),
        ),
    ]