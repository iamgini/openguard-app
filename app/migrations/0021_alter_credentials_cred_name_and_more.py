# Generated by Django 4.0.3 on 2022-03-10 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_managednodes_instance_credential'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentials',
            name='cred_name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='managednodes',
            name='instance_credential',
            field=models.CharField(default='-', max_length=50),
        ),
    ]
