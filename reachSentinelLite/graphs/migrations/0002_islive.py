# Generated by Django 2.0.2 on 2018-02-22 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsLive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isLive', models.BooleanField(default=False)),
            ],
        ),
    ]