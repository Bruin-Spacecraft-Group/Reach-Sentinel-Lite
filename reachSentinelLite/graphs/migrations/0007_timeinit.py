# Generated by Django 2.0.2 on 2018-05-02 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0006_delete_timeinit'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeInit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeInit', models.FloatField(default=0)),
            ],
        ),
    ]
