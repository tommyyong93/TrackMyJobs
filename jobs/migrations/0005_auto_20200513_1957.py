# Generated by Django 3.0.6 on 2020-05-13 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20200513_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
    ]
