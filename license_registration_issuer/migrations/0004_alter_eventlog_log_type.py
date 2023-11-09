# Generated by Django 4.2.7 on 2023-11-09 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_registration_issuer', '0003_eventlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='log_type',
            field=models.CharField(choices=[('SET_DATA', 'Set Data'), ('LICENSE_REGISTERED', 'License Registered'), ('LICENSE_REVOKED', 'License Revoked'), ('REQUIREMENT_REGISTERED', 'Requirement Registered'), ('REQUIREMENT_REVOKED', 'Requirement Revoked'), ('EVIDENCE_REGISTERED', 'Evidence Registered'), ('EVIDENCE_REVOKED', 'Evidence Revoked')], max_length=32),
        ),
    ]
