# Generated by Django 2.0.7 on 2018-08-25 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180825_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='games',
            field=models.ManyToManyField(blank=True, to='games.Game'),
        ),
    ]
