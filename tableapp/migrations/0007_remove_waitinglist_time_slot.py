# Generated by Django 5.1.1 on 2024-09-17 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tableapp', '0006_alter_waitinglist_time_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waitinglist',
            name='time_slot',
        ),
    ]
