# Generated by Django 4.0.2 on 2025-02-10 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syncer', '0010_alter_eventlog_log_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='additional_data_json',
            field=models.JSONField(default=dict),
        ),
    ]
