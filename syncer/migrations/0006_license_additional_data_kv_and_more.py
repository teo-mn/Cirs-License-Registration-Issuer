# Generated by Django 4.0.2 on 2023-12-18 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('syncer', '0005_evidence_additional_data_kv'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='additional_data_kv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='syncer.kv'),
        ),
        migrations.AddField(
            model_name='licenserequirements',
            name='additional_data_kv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='syncer.kv'),
        ),
    ]
