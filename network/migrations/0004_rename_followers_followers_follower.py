# Generated by Django 4.0.5 on 2022-09-13 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_following_followers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followers',
            old_name='followers',
            new_name='follower',
        ),
    ]