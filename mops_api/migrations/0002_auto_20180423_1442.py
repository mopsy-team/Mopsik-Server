# Generated by Django 2.0 on 2018-04-23 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mops_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mop',
            unique_together={('x', 'y', 'title', 'town', 'chainage')},
        ),
    ]
