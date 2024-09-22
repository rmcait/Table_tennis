# Generated by Django 5.1.1 on 2024-09-16 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tableapp', '0004_waitinglist_time_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='time_slot',
            field=models.CharField(blank=True, choices=[('9時 ~ 11時', '9時 ~ 11時'), ('11時 ~ 13時', '11時 ~ 13時'), ('13時 ~ 15時', '13時 ~ 15時'), ('15時 ~ 17時', '15時 ~ 17時'), ('17時 ~ 19時', '17時 ~ 19時'), ('19時 ~ 21時', '19時 ~ 21時')], max_length=20, null=True),
        ),
    ]
