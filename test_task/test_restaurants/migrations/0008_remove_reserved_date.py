# Generated by Django 2.2.4 on 2019-08-29 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_restaurants', '0007_auto_20190829_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserved',
            name='date',
        ),
    ]
