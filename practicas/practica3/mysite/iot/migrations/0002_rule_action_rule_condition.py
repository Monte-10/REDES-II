# Generated by Django 4.2.6 on 2024-04-11 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='action',
            field=models.CharField(default='No action defined', max_length=255),
        ),
        migrations.AddField(
            model_name='rule',
            name='condition',
            field=models.CharField(default='No condition defined', max_length=200),
        ),
    ]
