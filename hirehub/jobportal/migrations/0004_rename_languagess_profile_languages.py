# Generated by Django 5.0.6 on 2025-02-25 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0003_rename_certificate_description_profile_certificates_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='languagess',
            new_name='languages',
        ),
    ]
