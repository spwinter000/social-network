# Generated by Django 3.1.2 on 2021-01-13 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20210112_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=400, null=True),
        ),
    ]
