# Generated by Django 5.1.6 on 2025-02-27 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycoffeeapp', '0002_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='created_at',
        ),
    ]
