# Generated by Django 2.0.7 on 2018-08-10 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite1', '0003_auto_20180805_1620'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anime',
            old_name='update',
            new_name='time',
        ),
    ]