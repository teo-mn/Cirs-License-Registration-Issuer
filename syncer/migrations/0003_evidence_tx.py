# Generated by Django 4.2.7 on 2023-12-11 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syncer', '0002_remove_eventlog_contract_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evidence',
            name='tx',
            field=models.CharField(default='', max_length=128),
        ),
    ]
