# Generated by Django 4.0.2 on 2022-03-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_managednodes_instance_credential_to_use'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managednodes',
            name='instance_credential',
            field=models.CharField(choices=[('---', '---')], default='---', max_length=50),
        ),
    ]
