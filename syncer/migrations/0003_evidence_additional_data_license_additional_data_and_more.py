# Generated by Django 4.2.7 on 2023-12-01 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syncer', '0002_remove_latestsyncedblock_last_synced_block_kv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evidence',
            name='additional_data',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='license',
            name='additional_data',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='licenserequirements',
            name='additional_data',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
    ]
