# Generated by Django 2.1.2 on 2018-12-10 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20181210_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='', verbose_name='avatar'),
        ),
    ]
