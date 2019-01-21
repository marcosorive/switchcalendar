# Generated by Django 2.0.7 on 2018-08-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20180825_1007'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='deleted_account',
        ),
        migrations.AddField(
            model_name='profile',
            name='games',
            field=models.ManyToManyField(to='games.Game'),
        ),
    ]
