# Generated by Django 3.1.2 on 2020-12-24 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_following_likes_post'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Likes',
            new_name='Like',
        ),
    ]
