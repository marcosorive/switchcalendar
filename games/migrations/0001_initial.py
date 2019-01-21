# Generated by Django 2.0.7 on 2018-08-24 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('release_date', models.DateField(blank=True, default=None, null=True)),
                ('year_release', models.IntegerField(blank=True, default=None, null=True)),
                ('category', models.IntegerField(blank=True, choices=[(0, 'First Party'), (1, 'Third Party'), (2, 'Indie'), (3, 'Other')], null=True)),
                ('front_page', models.BooleanField(default=False)),
                ('switch_exclusive', models.NullBooleanField()),
                ('amz_link', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Optional.', max_length=30)),
                ('last_name', models.CharField(help_text='Optional.', max_length=30)),
                ('email', models.EmailField(help_text='Required. Inform a valid email address.', max_length=254)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]