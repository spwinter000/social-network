# Generated by Django 3.1.2 on 2021-01-12 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20210107_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=400),
        ),
    ]
