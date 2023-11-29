# Generated by Django 4.2.7 on 2023-11-29 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_registration_issuer', '0006_evidence_licenserequirements'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventLog',
        ),
        migrations.DeleteModel(
            name='Evidence',
        ),
        migrations.DeleteModel(
            name='LatestSyncedBlock',
        ),
        migrations.DeleteModel(
            name='License',
        ),
        migrations.DeleteModel(
            name='LicenseProduct',
        ),
        migrations.DeleteModel(
            name='LicenseRequirements',
        ),
        migrations.AlterField(
            model_name='request',
            name='request_type',
            field=models.CharField(choices=[('REGISTER', 'Register'), ('REVOKE', 'Revoke'), ('UPDATE_DURATION', 'Update Duration'), ('ADD_EMPLOYEE', 'Add Employee'), ('REMOVE_EMPLOYEE', 'Remove Employee'), ('ADD_REQUIREMENT', 'Add Requirement'), ('REMOVE_REQUIREMENT', 'Remove Requirement')], default='REGISTER', max_length=20),
        ),
    ]
