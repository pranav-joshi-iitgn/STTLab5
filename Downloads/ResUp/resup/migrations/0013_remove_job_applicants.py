# Generated by Django 4.0.6 on 2024-06-30 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resup', '0012_alter_application_resume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='applicants',
        ),
    ]
