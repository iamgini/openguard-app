# Generated by Django 4.0.3 on 2022-03-10 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_credentials_cred_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managednodes',
            name='instance_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='rules',
            name='rule_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
