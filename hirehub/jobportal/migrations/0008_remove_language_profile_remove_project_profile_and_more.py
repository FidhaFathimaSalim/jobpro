# Generated by Django 5.0.6 on 2025-02-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0007_rename_certificate_name_certificate_certificate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='project',
            name='profile',
        ),
        migrations.AddField(
            model_name='profile',
            name='language',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='project',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='project_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='project_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='certificate',
        ),
        migrations.DeleteModel(
            name='language',
        ),
        migrations.DeleteModel(
            name='project',
        ),
    ]
