# Generated by Django 4.2.14 on 2024-08-19 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_friends_status_messages_read'),
    ]

    operations = [
        migrations.DeleteModel(
            name='friends',
        ),
    ]
