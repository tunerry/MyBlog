# Generated by Django 2.0.7 on 2018-08-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite1', '0002_auto_20180804_1505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anime',
            old_name='seesion',
            new_name='quarter',
        ),
        migrations.AddField(
            model_name='anime',
            name='update',
            field=models.CharField(default='无', max_length=20),
        ),
    ]