# Generated by Django 2.2.4 on 2019-08-29 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_restaurants', '0008_remove_reserved_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserved',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='reserved',
            name='user',
        ),
    ]
