# Generated by Django 3.1.2 on 2021-01-20 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_auto_20210120_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(default='DEFAULT VALUE', max_length=400),
        ),
    ]
