# Generated by Django 3.0.6 on 2020-05-13 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20200513_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='date_onsite_interiew',
            new_name='date_onsite_interview',
        ),
    ]
