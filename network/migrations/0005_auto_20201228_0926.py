# Generated by Django 3.1.2 on 2020-12-28 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20201224_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='user',
        ),
        migrations.AddField(
            model_name='following',
            name='followed',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='followed_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='following',
            name='follower',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='follower_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='following',
            name='following',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]